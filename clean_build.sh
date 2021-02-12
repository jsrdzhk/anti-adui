#!/bin/sh

if [ -d build ]; then
  rm -dr build
fi
if [ -d dist ]; then
  rm -dr dist
fi
if [ -d src/anti-adui.egg-info ]; then
  rm -dr src/anti-adui.egg-info
fi
