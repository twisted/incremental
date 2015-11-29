my_project = 'exampleproj'

import os, importlib

def install_incremental():
    import importlib
    try:
        importlib.import_module('incremental')
    except ImportError:
        import pip
        pip.main(['install', 'incremental>=15.0.0'])
    finally:
        globals()['incremental'] = importlib.import_module('incremental')

install_incremental()

# PICK ONE OF:
# If you have a src/ dir
base_dir = os.path.dirname(__file__)
src_dir = os.path.join(base_dir, "src")
version = incremental.get_version_from_project(my_project, src_dir)

# Install the package

from setuptools import setup

setup(
    name=my_project,
    version=version.base()
)
