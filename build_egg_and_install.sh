#!/bin/sh

python3 setup.py bdist_egg
sudo easy_install dist/*.egg
source clean_build.sh
