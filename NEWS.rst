Incremental 24.11.0 (2025-11-27)
================================

Features
--------

- Incremental now provides a CLI script, ``incremental``, allowing you to run it with ``pipx run incremental``.
  The ``incremental update`` subcommand offers the same functionality as ``python -m incremental.update``. (`#99 <https://github.com/twisted/incremental/issues/99>`__)
- Incremental now depends on packaging instead of setuptools at runtime (`#141 <https://github.com/twisted/incremental/issues/141>`__)
- Add Python 3.13 and 3.14 to the test matrix. (`#179 <https://github.com/twisted/incremental/issues/179>`__)


Bugfixes
--------

- Build Incremental itself with Hatchling, working around failures with certain versions of setuptools (`#122 <https://github.com/twisted/incremental/issues/122>`__)


Improved Documentation
----------------------

- Incremental's documentation now highlights its primary features: CalVer and indeterminate versions (NEXT). (`#2 <https://github.com/twisted/incremental/issues/2>`__)


Deprecations and Removals
-------------------------

- Incremental's CLI no longer depends on Click, so you no longer need to install ``incremental[scripts]`` for it to function.
  The ``scripts`` extra is deprecated. (`#99 <https://github.com/twisted/incremental/issues/99>`__)
- Drop support for Python 3.8, which has been end-of-life since October 2024. (`#179 <https://github.com/twisted/incremental/issues/179>`__)


Misc
----

- `#105 <https://github.com/twisted/incremental/issues/105>`__, `#116 <https://github.com/twisted/incremental/issues/116>`__


Incremental 24.7.2 (2024-07-29)
===============================

Bugfixes
--------

- Incremental could mis-identify that a project had opted in to version management.

  If a ``pyproject.toml`` in the current directory contained a ``[project]`` table with a ``name`` key, but did not contain the opt-in ``[tool.incremental]`` table, Incremental would still treat the file as if the opt-in were present and attempt to validate the configuration. This could happen in contexts outside of packaging, such as when creating a virtualenv. When operating as a setuptools plugin Incremental now always ignores invalid configuration, such as configuration that doesn't match the content of the working directory. (`#106 <https://github.com/twisted/incremental/issues/106>`__)


Incremental 24.7.1 (2024-07-27)
===============================

Bugfixes
--------

- Incremental 24.7.0 would produce an error when parsing the ``pyproject.toml`` of a project that lacked the ``use_incremental=True`` or ``[tool.incremental]`` opt-in markers if that file lacked a ``[project]`` section containing the package name. This could cause a project that only uses ``pyproject.toml`` to configure tools to fail to build if Incremental is installed. Incremental now ignores such projects. (`#100 <https://github.com/twisted/incremental/issues/100>`__)


Misc
----

- `#101 <https://github.com/twisted/incremental/issues/101>`__


Incremental 24.7.0 (2024-07-25)
===============================

Features
--------

- Incremental can now be configured using ``pyproject.toml``. (`#90 <https://github.com/twisted/incremental/issues/90>`__)
- Incremental now provides a read-only `Hatchling version source plugin <https://hatch.pypa.io/latest/plugins/version-source/reference/>`_. (`#93 <https://github.com/twisted/incremental/issues/93>`__)


Bugfixes
--------

- Incremental no longer inserts a dot before the rc version component (i.e., ``1.2.3rc1`` instead of ``1.2.3.rc1``), resulting in version numbers in the `canonical format <https://packaging.python.org/en/latest/specifications/version-specifiers/#public-version-identifiers>`__. (`#81 <https://github.com/twisted/incremental/issues/81>`__)
- Incremental's tests are now included in the sdist release artifact. (`#80 <https://github.com/twisted/incremental/issues/80>`__)


Deprecations and Removals
-------------------------

- ``incremental[scripts]`` no longer depends on Twisted. (`#88 <https://github.com/twisted/incremental/issues/88>`__)
- Support for Python 2.7 has been dropped for lack of test infrastructure. We no longer provide universal wheels. (`#86 <https://github.com/twisted/incremental/issues/86>`__)
- Support for Python 3.5, 3.6, and 3.7 has been dropped for lack of test infrastructure. (`#92 <https://github.com/twisted/incremental/issues/92>`__)


Incremental 22.10.0 (2022-10-15)
================================

No significant changes.


Incremental 22.10.0.rc1 (2022-10-04)
====================================

Features
--------

- Incremental now supports type-checking with Mypy (#69)


Incremental 21.3.0 (2021-03-01)
===============================

Bugfixes
--------

- The output of incremental is now compatible with Black (#56, #60)
- Incremental now properly supports PEP 440-compliant dev, rc, post suffixes (#62)
- Incremental now properly supports PEP 440-compliant post releases (#37)


Incremental 17.5.0 (2017-05-20)
===============================

Deprecations and Removals
-------------------------

- Incremental will no longer attempt to read git or svn repositories to see if
  the project is running from a checkout. (#30, #31, #32)


Incremental 16.10.1 (2016-10-20)
================================

Bugfixes
--------

- Comparisons of Versions now compare the lowercased forms of both
  version packages, rather than being case sensitive. (#23)


Incremental 16.10.0 (2016-10-10)
================================

Bugfixes
--------

- incremental.update now adds a docstring to the autogenerated file.
  (#18)

Misc
----

- #20


Incremental 16.9.1 (2016-09-21)
===============================

Bugfixes
--------

- python -m incremental.update <package> --dev now starts a dev-less
  package at 0, not 1. (#15)


Incremental 16.9.0 (2016-09-18)
===============================

Features
--------

- Incremental now uses 'rcX' instead of 'pre' for prereleases/release
  candidates, to match PEP440. (#4)
- If you reference "<yourproject> NEXT" and use `python -m
  incremental.update`, it will automatically be updated to the next
  release version number. (#7)

Misc
----

- #1, #10
