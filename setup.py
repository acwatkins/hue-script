#!/usr/bin/env python3

from setuptools import setup

setup(name='setuplightschedule',
      version='0.0.0.1',
      description='A personal schedule for my lights',
      url='https://github.com/acwatkins/setuplightschedule',
      author='Adam Watkins',
      author_email='acwatkins@gmail.com',
      license='GPL3',
      scripts=['bin/setuplightschedule'],
      install_requires = ['hues>=0.0.0.2'])
