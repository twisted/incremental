#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import os, sys

from setuptools import setup, find_packages

setup(
    name='eventually',
    maintainer='Amber Brown',
    maintainer_email='hawkowl@twistedmatrix.com',
    url="https://github.com/twisted/eventually",
    classifiers = [
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
    ],
    use_incremental=True,
    setup_requires=['incremental'],
    install_requires=[
        'incremental'
    ],
    package_dir={"": "src"},
    packages=find_packages('src'),
    license="MIT",
    zip_safe=False,
    include_package_data=True,
    description='Deprecation support for Python.',
    long_description=open('README.rst').read(),
)
