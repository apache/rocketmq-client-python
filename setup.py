#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


readme = 'README.md'
with open(readme) as f:
    long_description = f.read()

setup(
    name='rocketmq',
    version='0.0.0',
    author='messense',
    author_email='messense@icloud.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    keywords='rocketmq',
    description='RocketMQ Python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
)
