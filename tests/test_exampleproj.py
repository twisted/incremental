# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for L{incremental._versioning}.
"""

from __future__ import division, absolute_import

from twisted.trial.unittest import TestCase


class ExampleProjTests(TestCase):
    def test_version(self):
        """
        exampleproj has a version of 1.2.3.
        """
        import exampleproj

        self.assertEqual(exampleproj.__version__.base(), "1.2.3")
