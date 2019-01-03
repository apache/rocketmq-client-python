#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

from setuptools import setup, find_packages


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
    python_requires='>=3.6',
    classifiers=[
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
