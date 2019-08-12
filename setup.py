#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import struct

from setuptools import setup, find_packages
from setuptools.command.install import install


readme = 'README.md'
with open(readme) as f:
    long_description = f.read()

# from https://stackoverflow.com/questions/45150304/how-to-force-a-python-wheel-to-be-platform-specific-when-building-it # noqa
cmdclass = {}
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel

    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            # Mark us as not a pure python package (we have platform specific C/C++ code)
            self.root_is_pure = False

        def get_tag(self):
            # this set's us up to build generic wheels.
            python, abi, plat = _bdist_wheel.get_tag(self)
            python, abi = 'py2.py3', 'none'
            return python, abi, plat
    cmdclass['bdist_wheel'] = bdist_wheel

except ImportError:
    pass

class InstallPlatlib(install):
    def finalize_options(self):
        install.finalize_options(self)
        # force platlib
        self.install_lib = self.install_platlib

cmdclass['install'] = InstallPlatlib

setup(
    name='rocketmq',
    version='0.3.15',
    author='messense',
    author_email='messense@icloud.com',
    packages=find_packages(exclude=('tests', 'tests.*')),
    keywords='rocketmq',
    description='RocketMQ Python client',
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    install_requires=[
        "enum34; python_version<='3.4'",
    ],
    cmdclass=cmdclass,
    classifiers=[
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
