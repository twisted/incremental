# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{incremental._versioning}.
"""

from __future__ import division, absolute_import

from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase

from incremental.update import _run


class NonCreatedUpdateTests(TestCase):

    def setUp(self):

        self.srcdir = FilePath(self.mktemp())
        self.srcdir.makedirs()

        packagedir = self.srcdir.child('inctestpkg')
        packagedir.makedirs()

        packagedir.child('__init__.py').setContent(b"""
from incremental import Version
introduced_in = Version('inctestpkg', 'NEXT', 0, 0).short()
next_released_version = "inctestpkg NEXT"
""")
        self.getcwd = lambda: self.srcdir.path
        self.packagedir = packagedir

        class Date(object):
            year = 2016
            month = 8

        self.date = Date()

    def test_create(self):
        """
        `incremental.update package --create` initialises the version.
        """
        self.assertFalse(self.packagedir.child("_version.py").exists())

        out = []
        _run('inctestpkg', path=None, newversion=None, patch=False, rc=False,
             dev=False, create=True, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertTrue(self.packagedir.child("_version.py").exists())
        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 16, 8, 0)
__all__ = ["__version__"]
""")

class MissingTests(TestCase):

    def setUp(self):

        self.srcdir = FilePath(self.mktemp())
        self.srcdir.makedirs()

        self.srcdir.child('srca').makedirs()

        packagedir = self.srcdir.child('srca').child('inctestpkg')
        packagedir.makedirs()

        packagedir.child('__init__.py').setContent(b"""
from incremental import Version
introduced_in = Version('inctestpkg', 'NEXT', 0, 0).short()
next_released_version = "inctestpkg NEXT"
""")
        packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3)
__all__ = ["__version__"]
""")
        self.getcwd = lambda: self.srcdir.path
        self.packagedir = packagedir

        class Date(object):
            year = 2016
            month = 8

        self.date = Date()

    def test_path(self):
        """
        `incremental.update package --dev` raises and quits if it can't find
        the package.
        """
        out = []
        with self.assertRaises(ValueError):
            _run(u'inctestpkg', path=None, newversion=None,
                patch=False, rc=False, dev=True, create=False, _date=self.date,
                _getcwd=self.getcwd, _print=out.append)


class CreatedUpdateInSrcTests(TestCase):

    def setUp(self):

        self.srcdir = FilePath(self.mktemp())
        self.srcdir.makedirs()

        self.srcdir.child('src').makedirs()

        packagedir = self.srcdir.child('src').child('inctestpkg')
        packagedir.makedirs()

        packagedir.child('__init__.py').setContent(b"""
from incremental import Version
introduced_in = Version('inctestpkg', 'NEXT', 0, 0).short()
next_released_version = "inctestpkg NEXT"
""")
        packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3)
__all__ = ["__version__"]
""")
        self.getcwd = lambda: self.srcdir.path
        self.packagedir = packagedir

        class Date(object):
            year = 2016
            month = 8

        self.date = Date()

    def test_path(self):
        """
        `incremental.update package --path=<path> --dev` increments the dev
        version of the package on the given path
        """
        out = []
        _run(u'inctestpkg', path=None, newversion=None,
             patch=False, rc=False, dev=True, create=False, _date=self.date,
             _getcwd=self.getcwd, _print=out.append)

        self.assertTrue(self.packagedir.child("_version.py").exists())
        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 3, dev=1)
__all__ = ["__version__"]
""")


class CreatedUpdateTests(TestCase):

    maxDiff = None

    def setUp(self):

        self.srcdir = FilePath(self.mktemp())
        self.srcdir.makedirs()

        packagedir = self.srcdir.child('inctestpkg')
        packagedir.makedirs()

        packagedir.child('__init__.py').setContent(b"""
from incremental import Version
introduced_in = Version('inctestpkg', 'NEXT', 0, 0).short()
next_released_version = "inctestpkg NEXT"
""")
        packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3)
__all__ = ["__version__"]
""")
        self.getcwd = lambda: self.srcdir.path
        self.packagedir = packagedir

        class Date(object):
            year = 2016
            month = 8

        self.date = Date()

    def test_path(self):
        """
        `incremental.update package --path=<path> --dev` increments the dev
        version of the package on the given path
        """
        out = []
        _run(u'inctestpkg', path=self.packagedir.path, newversion=None,
             patch=False, rc=False, dev=True, create=False, _date=self.date,
             _print=out.append)

        self.assertTrue(self.packagedir.child("_version.py").exists())
        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 3, dev=1)
__all__ = ["__version__"]
""")

    def test_dev(self):
        """
        `incremental.update package --dev` increments the dev version.
        """
        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=False, rc=False,
             dev=True, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertTrue(self.packagedir.child("_version.py").exists())
        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 3, dev=1)
__all__ = ["__version__"]
""")

    def test_patch(self):
        """
        `incremental.update package --patch` increments the patch version.
        """
        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=True, rc=False,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 4)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 1, 2, 4).short()
next_released_version = "inctestpkg 1.2.4"
""")

    def test_patch_with_prerelease_and_dev(self):
        """
        `incremental.update package --patch` increments the patch version, and
        disregards any old prerelease/dev versions.
        """
        self.packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3, release_candidate=1, dev=2)
__all__ = ["__version__"]
""")

        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=True, rc=False,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 4)
__all__ = ["__version__"]
""")
    def test_rc_patch(self):
        """
        `incremental.update package --patch --rc` increments the patch
        version and makes it a release candidate.
        """
        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=True, rc=True,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 4, release_candidate=1)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 1, 2, 4, release_candidate=1).short()
next_released_version = "inctestpkg 1.2.4rc1"
""")

    def test_rc_with_existing_rc(self):
        """
        `incremental.update package --rc` increments the rc version if the
        existing version is an rc, and discards any dev version.
        """
        self.packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3, release_candidate=1, dev=2)
__all__ = ["__version__"]
""")

        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=False, rc=True,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 1, 2, 3, release_candidate=2)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 1, 2, 3, release_candidate=2).short()
next_released_version = "inctestpkg 1.2.3rc2"
""")

    def test_rc_with_no_rc(self):
        """
        `incremental.update package --rc`, when the package is not a release
        candidate, will issue a new major/minor rc, and disregards the micro
        and dev.
        """
        self.packagedir.child('_version.py').setContent(b"""
from incremental import Version
__version__ = Version('inctestpkg', 1, 2, 3, dev=2)
__all__ = ["__version__"]
""")

        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=False, rc=True,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 16, 8, 0, release_candidate=1)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 16, 8, 0, release_candidate=1).short()
next_released_version = "inctestpkg 16.8.0rc1"
""")

    def test_full_with_rc(self):
        """
        `incremental.update package`, when the package is a release
        candidate, will issue the major/minor, sans release candidate or dev.
        """
        out = []
        _run(u'inctestpkg', path=None, newversion=None, patch=False, rc=True,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 16, 8, 0, release_candidate=1)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 16, 8, 0, release_candidate=1).short()
next_released_version = "inctestpkg 16.8.0rc1"
""")

        _run(u'inctestpkg', path=None, newversion=None, patch=False, rc=False,
             dev=False, create=False, _date=self.date, _getcwd=self.getcwd,
             _print=out.append)

        self.assertEqual(self.packagedir.child("_version.py").getContent(),
                         b"""# This file is auto-generated! Do not edit!
# Use `python -m incremental.update inctestpkg` to change this file.

from incremental import Version

__version__ = Version('inctestpkg', 16, 8, 0)
__all__ = ["__version__"]
""")
        self.assertEqual(self.packagedir.child("__init__.py").getContent(),
                         b"""
from incremental import Version
introduced_in = Version('inctestpkg', 16, 8, 0).short()
next_released_version = "inctestpkg 16.8.0"
""")
