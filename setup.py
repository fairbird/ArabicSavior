#!/usr/bin/python
# -*- coding: utf-8 -*-
from distutils.core import setup

PLUGIN_DIR = 'Extensions.ArabicSavior'

setup(name='enigma2-plugin-extensions-ArabicSavior',
       version='1.0',
       author='RAED',
       author_email='rrrr53@hotmail.com',
       description='plugin to fix arabic fonts and also to changing fonts type.',
       packages=[PLUGIN_DIR],
       package_dir={PLUGIN_DIR: 'usr'},
       package_data={PLUGIN_DIR: ['plugin.png', '*/*.png']},
      )
