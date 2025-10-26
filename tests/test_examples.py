# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Tests for the packaging examples.
"""

import os
from importlib import metadata
from subprocess import run
from tempfile import TemporaryDirectory

from build import BuildBackendException, ProjectBuilder
from build.env import DefaultIsolatedEnv
from twisted.python.filepath import FilePath
from twisted.trial.unittest import TestCase

from incremental import Version

TEST_DIR = FilePath(os.path.abspath(os.path.dirname(__file__)))


def build_and_install(path: FilePath) -> None:
    with TemporaryDirectory(prefix="dist") as dist_dir:
        with DefaultIsolatedEnv(installer="pip") as env:
            env.install(
                {
                    # Install the *exact* version of Incremental under test.
                    # Otherwise pip might select a different version from
                    # its cache.
                    #
                    # These are formally PEP 508 markers, so we pass a
                    # file URL.
                    "incremental @ file://" + os.environ["TOX_PACKAGE"],
                    # A .pth file so that subprocess generate coverage.
                    "coverage-p",
                }
            )
            builder = ProjectBuilder.from_isolated_env(env, path.path)
            env.install(builder.build_system_requires)
            env.install(builder.get_requires_for_build("wheel", {}))
            pkgfile = builder.build("wheel", output_directory=dist_dir)

        # Force reinstall in case tox reused the venv.
        run(["pip", "install", "--force-reinstall", pkgfile], check=True)


class ExampleTests(TestCase):
    def test_setuppy_version(self):
        """
        example_setuppy has a version of 1.2.3.
        """
        build_and_install(TEST_DIR.child("example_setuppy"))

        import example_setuppy

        self.assertEqual(example_setuppy.__version__.base(), "1.2.3")
        self.assertEqual(metadata.version("example_setuppy"), "1.2.3")

    def test_setuptools_version(self):
        """
        example_setuptools has a version of 2.3.4.
        """
        build_and_install(TEST_DIR.child("example_setuptools"))

        import example_setuptools

        self.assertEqual(example_setuptools.__version__.base(), "2.3.4")
        self.assertEqual(metadata.version("example_setuptools"), "2.3.4")

    def test_setuptools_no_optin(self):
        """
        The setuptools plugin is a no-op when there isn't a
        [tool.incremental] table in pyproject.toml.
        """
        src = FilePath(self.mktemp())
        src.makedirs()
        src.child("pyproject.toml").setContent(
            b"""\
[project]
name = "example_no_optin"
version = "0.0.0"
"""
        )
        package_dir = src.child("example_no_optin")
        package_dir.makedirs()
        package_dir.child("__init__.py").setContent(b"")
        package_dir.child("_version.py").setContent(
            b"from incremental import Version\n"
            b'__version__ = Version("example_no_optin", 24, 7, 0)\n'
        )

        build_and_install(src)

        self.assertEqual(metadata.version("example_no_optin"), "0.0.0")

    def test_setuptools_no_package(self):
        """
        The setuptools plugin is a no-op when there isn't a
        package directory that matches the project name.
        """
        src = FilePath(self.mktemp())
        src.makedirs()
        src.child("pyproject.toml").setContent(
            b"""\
[project]
name = "example_no_package"
version = "0.0.0"

[tool.incremental]
"""
        )

        build_and_install(src)

        self.assertEqual(metadata.version("example_no_package"), "0.0.0")

    def test_setuptools_missing_versionpy(self):
        """
        The setuptools plugin is a no-op when the ``_version.py`` file
        isn't present.
        """
        src = FilePath(self.mktemp())
        src.makedirs()
        src.child("setup.py").setContent(
            b"""\
from setuptools import setup

setup(
    name="example_missing_versionpy",
    version="0.0.1",
    packages=["example_missing_versionpy"],
    zip_safe=False,
)
"""
        )
        src.child("pyproject.toml").setContent(
            b"""\
[tool.incremental]
name = "example_missing_versionpy"
"""
        )
        package_dir = src.child("example_missing_versionpy")
        package_dir.makedirs()
        package_dir.child("__init__.py").setContent(b"")
        # No _version.py exists

        build_and_install(src)

        # The version from setup.py wins.
        self.assertEqual(metadata.version("example_missing_versionpy"), "0.0.1")

    def test_setuptools_bad_versionpy(self):
        """
        The setuptools plugin surfaces syntax errors in ``_version.py``.
        """
        src = FilePath(self.mktemp())
        src.makedirs()
        src.child("setup.py").setContent(
            b"""\
from setuptools import setup

setup(
    name="example_bad_versionpy",
    version="0.1.2",
    packages=["example_bad_versionpy"],
    zip_safe=False,
)
"""
        )
        src.child("pyproject.toml").setContent(
            b"""\
[tool.incremental]
name = "example_bad_versionpy"
"""
        )
        package_dir = src.child("example_bad_versionpy")
        package_dir.makedirs()
        package_dir.child("_version.py").setContent(b"bad version.py")

        with self.assertRaises(BuildBackendException):
            # This also spews a SyntaxError traceback to stdout.
            build_and_install(src)

    def test_hatchling_get_version(self):
        """
        example_hatchling has a version of 24.7.0.
        """
        build_and_install(TEST_DIR.child("example_hatchling"))

        import example_hatchling

        self.assertEqual(
            example_hatchling.__version__,
            Version("example_hatchling", 24, 7, 0),
        )
        self.assertEqual(metadata.version("example_hatchling"), "24.7.0")

    def test_hatch_version(self):
        """
        The ``hatch version`` command reports the version of a package
        packaged with hatchling.
        """
        proc = run(
            ["hatch", "version"],
            cwd=TEST_DIR.child("example_hatchling").path,
            check=True,
            capture_output=True,
        )

        self.assertEqual(proc.stdout, b"24.7.0\n")

    def test_hatch_version_set(self):
        """
        The ``hatch version`` command can't set the version so its output
        tells the user to use ``incremental`` instead.
        """
        proc = run(
            ["hatch", "--no-color", "version", "24.8.0"],
            cwd=TEST_DIR.child("example_hatchling").path,
            check=False,
            capture_output=True,
        )
        suggestion = b"Run `incremental update example_hatchling --newversion 24.8.0` to set the version."

        self.assertGreater(proc.returncode, 0)
        self.assertRegex(
            proc.stdout,
            # Hatch may wrap the output, so we are flexible about the specifics of whitespace.
            suggestion.replace(b".", rb"\.").replace(b" ", b"\\s+"),
        )

    def test_noop(self):
        """
        The Incremental setuptools hook is a silent no-op when there is no Incremental
        configuration to be found.
        """
        build_and_install(TEST_DIR.child("example_noop"))

        import example_noop

        self.assertEqual(example_noop.__version__, "100")
        self.assertEqual(metadata.version("example_noop"), "100")
