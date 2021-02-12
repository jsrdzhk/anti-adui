# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : main.py
# Time       ：2/9/21 14:43
# Author     ：Rodney Cheung
"""
import argparse
import json
import os
from os.path import abspath, dirname
from typing import List, Dict

import pkg_resources
from adbutils_wrapper.adb import AdbUtilWrapper, AdbTool
from loguru import logger


class RedundantApk:
    def __init__(self, ad=None, game=None, input_method=None, media=None, tool=None,
                 third_party=None, bug_report=None, browser=None, global_service=None,
                 pay=None, assistant=None, theme=None, unknown=None):
        self.__uninstalled_apps: Dict[str, List[str]] = {
            'ad': ad,
            'game': game,
            'input_method': input_method,
            'media': media,
            'tool': tool,
            'third_party': third_party,
            'bug_report': bug_report,
            'browser': browser,
            'global_service': global_service,
            'pay': pay,
            'assistant': assistant,
            'theme': theme,
            'unknown': unknown
        }
        # self.__ad: List[str] = ad
        # self.__game: List[str] = game
        # self.__input_method: List[str] = input_method
        # self.__media: List[str] = media
        # self.__tool: List[str] = tool
        # self.__third_party: List[str] = third_party
        # self.__bug_report: List[str] = bug_report
        # self.__browser: List[str] = browser
        # self.__global_service: List[str] = global_service
        # self.__pay: List[str] = pay
        # self.__assistant: List[str] = assistant
        # self.__theme: List[str] = theme
        # self.__unknown: List[str] = unknown

    @property
    def uninstalled_apps(self):
        return self.__uninstalled_apps

    @uninstalled_apps.setter
    def uninstalled_apps(self, value):
        self.__uninstalled_apps = value

    # @property
    # def ad(self):
    #     return self.__ad
    #
    # @ad.setter
    # def ad(self, value):
    #     self.__ad = value
    #
    # @property
    # def game(self):
    #     return self.__game
    #
    # @game.setter
    # def game(self, value):
    #     self.__game = value
    #
    # @property
    # def input_method(self):
    #     return self.__input_method
    #
    # @input_method.setter
    # def input_method(self, value):
    #     self.__input_method = value
    #
    # @property
    # def media(self):
    #     return self.__media
    #
    # @media.setter
    # def media(self, value):
    #     self.__media = value
    #
    # @property
    # def tool(self):
    #     return self.__tool
    #
    # @tool.setter
    # def tool(self, value):
    #     self.__tool = value
    #
    # @property
    # def third_party(self):
    #     return self.__third_party
    #
    # @third_party.setter
    # def third_party(self, value):
    #     self.__third_party = value
    #
    # @property
    # def bug_report(self):
    #     return self.__bug_report
    #
    # @bug_report.setter
    # def bug_report(self, value):
    #     self.__bug_report = value
    #
    # @property
    # def browser(self):
    #     return self.__browser
    #
    # @browser.setter
    # def browser(self, value):
    #     self.__browser = value
    #
    # @property
    # def global_service(self):
    #     return self.__global_service
    #
    # @global_service.setter
    # def global_service(self, value):
    #     self.__global_service = value
    #
    # @property
    # def pay(self):
    #     return self.__pay
    #
    # @pay.setter
    # def pay(self, value):
    #     self.__pay = value
    #
    # @property
    # def assistant(self):
    #     return self.__assistant
    #
    # @assistant.setter
    # def assistant(self, value):
    #     self.__assistant = value
    #
    # @property
    # def theme(self):
    #     return self.__theme
    #
    # @theme.setter
    # def theme(self, value):
    #     self.__theme = value
    #
    # @property
    # def unknown(self):
    #     return self.__unknown
    #
    # @unknown.setter
    # def unknown(self, value):
    #     self.__unknown = value


def exit_process():
    os.kill(os.getpid(), 9)


def choose_device(adb_util_wrapper: AdbUtilWrapper) -> str:
    device_id_list = adb_util_wrapper.device_id_list()
    if not device_id_list:
        print('请插入adb设备！')
        exit_process()

    if len(device_id_list) == 1:
        logger.info('默认选取adb工作设备： {}', device_id_list[0])
        return device_id_list[0]
    else:
        msg = '请选择工作设备： {0}'.format(os.linesep)
        for i in range(len(device_id_list)):
            msg += '{0}\t{1}{2}'.format(i + 1, device_id_list[i], os.linesep)
        logger.info(msg)
        while True:
            index = int(input("选择工作设备id:")) - 1
            if (0 > index) or (index >= len(device_id_list)):
                logger.error('id输入错误')
            else:
                logger.info('已选取adb工作设备:{}', device_id_list[index])
                return device_id_list[index]


def load_config() -> RedundantApk:
    conf_path = os.path.join(dirname(abspath(__file__)), 'config.json')
    with open(conf_path, 'rb') as f:
        loaded = json.load(f)['miui']
        return RedundantApk(loaded['ad'], loaded['game'], loaded['input_method'], loaded['media'], loaded['tool'],
                            loaded['third_party'],
                            loaded['bug_report'], loaded['browser'], loaded['global_service'], loaded['pay'],
                            loaded['assistant'], loaded['theme'],
                            loaded['unknown'])


def uninstall(redundant_apps: RedundantApk, uninstalled_apps: str, adb_tool: AdbTool):
    need_uninstalled_apps = list()
    supported_app_types = redundant_apps.uninstalled_apps.keys()
    if uninstalled_apps == 'all':
        for supported_app_type in supported_app_types:
            need_uninstalled_apps.extend(redundant_apps.uninstalled_apps[supported_app_type])
    else:
        need_uninstalled_types = uninstalled_apps.split(',')
        for need_uninstalled_type in need_uninstalled_types:
            if need_uninstalled_type in supported_app_types:
                need_uninstalled_apps.extend(redundant_apps.uninstalled_apps[need_uninstalled_type])
            else:
                logger.warning('unsupported app type:{}', need_uninstalled_type)
    pm = adb_tool.package_manager
    am = adb_tool.activity_manager
    actually_uninstalled_apps = pm.uninstall_apps_for_user(am.get_current_user_id(), need_uninstalled_apps)
    logger.info('uninstalled apps:')
    for actually_uninstalled_app in actually_uninstalled_apps:
        logger.info(actually_uninstalled_app)


def main():
    parser = argparse.ArgumentParser(description='anti adui')
    parser.add_argument('-i', '--host',
                        default='127.0.0.1',
                        type=str,
                        help='adb host',
                        dest='host')
    parser.add_argument('-p', '--port',
                        default=5037,
                        type=int,
                        help='adb port',
                        dest='port')
    parser.add_argument('-u', '--uninstalled-app',
                        default='all',
                        type=str,
                        help='uninstall which',
                        dest='uninstalled_apps')
    parser.add_argument('-v', '--version',
                        default=False,
                        action="store_true",
                        help="show anti_adui version",
                        dest='version')
    args = parser.parse_known_args()
    version = args[0].version
    if version:
        pc_tool_version = pkg_resources.get_distribution('anti_adui')
        print(pc_tool_version)
        return
    logger.add('anti_adui.log', rotation='1 MB')
    host = args[0].host
    port = args[0].port
    uninstalled_apps: str = args[0].uninstalled_apps
    adb_util_wrapper = AdbUtilWrapper(host, port)
    chosen_device_id = choose_device(adb_util_wrapper)
    adb_tool = adb_util_wrapper.adb_tool(chosen_device_id)
    redundant_apps = load_config()
    uninstall(redundant_apps, uninstalled_apps, adb_tool)


if __name__ == '__main__':
    main()
