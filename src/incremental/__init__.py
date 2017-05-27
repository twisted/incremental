# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Versioning & deprecation for Python packages.

To create a Version, call it with a package name and version number parts::

    >>> from incremental import Version
    >>> myVer = Version("MyProj", 1, 2, 3)
    >>> print(myVer.public())
    1.2.3

Other functions are available for getting "human friendly" version strings for
your app::

    >>> from incremental import getVersionString, Version
    >>> myVer = Version("MyProj", 17, 5, 1, dev=0)
    >>> print(getVersionString(myVer))
    MyProj 17.5.1dev0

Versions are also comparable::

    >>> v1 = Version("MyProj", 17, 5, 0)
    >>> v2 = Version("MyProj", 17, 6, 0)
    >>> v1 > v2
    False
    >>> v2 > v1
    True
    >>> v1 == v2
    False

To mark a method, function, or class as being deprecated do this::

    from incremental import Version, deprecated

    @deprecated(Version("MyProj", 8, 0, 0))
    def badAPI(self, first, second):
        '''
        Docstring for badAPI.
        '''
        ...
    @deprecated(Version("MyProj", 16, 0, 0))
    class BadClass(object):
        '''
        Docstring for BadClass.
        '''

The newly-decorated badAPI will issue a warning when called, and BadClass will
issue a warning when instantiated.  Both will also have a deprecation notice
appended to their docstring.  To deprecate properties you can use::

    from incremental import Version, deprecatedProperty

    class OtherwiseUndeprecatedClass(object):
        @deprecatedProperty(Version('MyProj', 16, 0, 0))
        def badProperty(self):
            '''
            Docstring for badProperty.
            '''
        @badProperty.setter
        def badProperty(self, value):
            '''
            Setter sill also raise the deprecation warning.
            '''

To mark module-level attributes as being deprecated you can use::

    badAttribute = "someValue"
    ...
    deprecatedModuleAttribute(
        Version("MyProj", 8, 0, 0),
        "Use goodAttribute instead.",
        "your.full.module.name",
        "badAttribute")

The deprecated attributes will issue a warning whenever they are accessed.  If
the attributes being deprecated are in the same module as the
L{deprecatedModuleAttribute} call is being made from, the C{__name__} global
can be used as the C{moduleName} parameter.  See also L{incremental.Version}.

@type DEPRECATION_WARNING_FORMAT: C{str}
@var DEPRECATION_WARNING_FORMAT: The default deprecation warning string format
    to use when one is not provided by the user.
"""

from __future__ import division, absolute_import

from ._versioning import (
    Version,
    getVersionString,
    IncomparableVersions,
    _inf,
    _get_version,
)
from ._deprecate import (
    getDeprecationWarningString,
    deprecated,
    deprecatedProperty,
    deprecatedModuleAttribute,
    DEPRECATION_WARNING_FORMAT,
    warnAboutFunction,
    getWarningMethod,
    setWarningMethod
)
from ._version import __version__ # noqa


__all__ = [
    "Version",
    "getVersionString",
    "IncomparableVersions",
    "getDeprecationWarningString",
    "deprecated",
    "deprecatedProperty",
    "deprecatedModuleAttribute",
    "DEPRECATION_WARNING_FORMAT",
    "warnAboutFunction",
    "getWarningMethod",
    "setWarningMethod",
    "__version__"
]
