#!/usr/bin/env python

from __future__ import absolute_import, division, print_function

import os
import sys

from setuptools import setup

base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")

# We need to import outselves
sys.path.insert(0, src_dir)

import incremental

setup(version=incremental.__version__.base())
