Incremental
===========

|travis|
|pypi|
|coverage|

Incremental is a small library that versions your Python projects.


Quick Start
-----------

Add this to the top of your ``setup.py``, assuming your code is called ``widgetbox``:

.. code::

    my_project = 'widgetbox'

    import os, importlib

    def install_incremental():
        import importlib
        try:
            importlib.import_module('incremental')
        except ImportError:
            import pip
            pip.main(['install', 'incremental>=0.1.0'])
        finally:
            globals()['incremental'] = importlib.import_module('incremental')

    install_incremental()

    # PICK ONE OF:
    # If you have a src/ dir
    base_dir = os.path.dirname(__file__)
    src_dir = os.path.join(base_dir, "src")
    # If you do not
    src_dir = os.path.dirname(__file__)

    version = incremental.get_version_from_project(my_project, src_dir)

And in the ``setup`` call, add:

.. code::

   setup(
       name=my_project,
       version=version.base(),
       ...
   }

Then in your project add a ``_version.py`` that contains:

.. code::

   from incremental import Version

   __version__ = Version("widgetbox", 1, 2, 3)
   __all__ = ["__version__"]


Then in your project's ``__init__.py`` add:

.. code::

   from ._version import __version__


Subsequent installations of your project will use incremental for versioning.

.. |coverage| image:: https://codecov.io/github/hawkowl/incremental/coverage.svg?branch=master
.. _coverage: https://codecov.io/github/hawkowl/incremental

.. |travis| image:: https://travis-ci.org/hawkowl/incremental.svg?branch=master
.. _travis: http://travis-ci.org/hawkowl/incremental

.. |pypi| image:: http://img.shields.io/pypi/v/incremental.svg
.. _pypi: https://pypi.python.org/pypi/incremental
