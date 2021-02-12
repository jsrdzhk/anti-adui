# !/usr/bin/env python3
# -*-coding:utf-8 -*-

"""
# File       : setup.py
# Time       ：2/9/21 14:43
# Author     ：Rodney Cheung
"""

import os

import setuptools


def find_version(file_name):
    with open(file_name, encoding='utf-8') as file_handle:
        lines = file_handle.readlines()
        latest_version = lines[0].strip(os.linesep).rstrip(']').lstrip('[')
        print("anti_adui:", latest_version)
        return latest_version


setuptools.setup(
    name='anti_adui',
    version=find_version("./ChangeLog"),
    description='anti adui',
    long_description='anti adui',
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(where='src', include=[
        'anti_adui', 'anti_adui.*'
    ]),
    package_dir={'': 'src'},
    install_requires=[
        'adbutils',
    ],
    package_data={
        '': ['config.json']
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "anti-adui = anti_adui.main:main",
        ]
    },
    python_requires='>=3.7,<3.9',
    platforms=['any'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Utilities',
    ],
    zip_safe=False)
