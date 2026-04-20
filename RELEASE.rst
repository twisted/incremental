Releasing Incremental
=====================

To release Incremental, `install just <https://just.systems/>`_ and run `just release`.

This will bump the version,
render `the changelog <./NEWS.rst>`_,
and push the tagged release.
The `release workflow <https://github.com/twisted/incremental/actions/workflows/release.yml>`_
will build and upload the library to PyPI.org.
