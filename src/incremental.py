# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

"""
Versions for Python packages.

See L{Version}.
"""

from __future__ import division, absolute_import

import os
import sys

#
# Compat functions
#

if sys.version_info < (3, 0):
    _PY3 = False
else:
    _PY3 = True


def nativeString(s):
    """
    Convert C{bytes} or C{unicode} to the native C{str} type, using ASCII
    encoding if conversion is necessary.

    @raise UnicodeError: The input string is not ASCII encodable/decodable.
    @raise TypeError: The input is neither C{bytes} nor C{unicode}.
    """
    if not isinstance(s, (bytes, unicode)):
        raise TypeError("%r is neither bytes nor unicode" % s)
    if _PY3:
        if isinstance(s, bytes):
            return s.decode("ascii")
        else:
            # Ensure we're limited to ASCII subset:
            s.encode("ascii")
    else:
        if isinstance(s, unicode):
            return s.encode("ascii")
        else:
            # Ensure we're limited to ASCII subset:
            s.decode("ascii")
    return s


try:
    cmp = cmp
except NameError:
    def cmp(a, b):
        """
        Compare two objects.

        Returns a negative number if C{a < b}, zero if they are equal, and a
        positive number if C{a > b}.
        """
        if a < b:
            return -1
        elif a == b:
            return 0
        else:
            return 1


def comparable(klass):
    """
    Class decorator that ensures support for the special C{__cmp__} method.

    On Python 2 this does nothing.

    On Python 3, C{__eq__}, C{__lt__}, etc. methods are added to the class,
    relying on C{__cmp__} to implement their comparisons.
    """
    # On Python 2, __cmp__ will just work, so no need to add extra methods:
    if not _PY3:
        return klass

    def __eq__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c == 0

    def __ne__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c != 0

    def __lt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c < 0

    def __le__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c <= 0

    def __gt__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c > 0

    def __ge__(self, other):
        c = self.__cmp__(other)
        if c is NotImplemented:
            return c
        return c >= 0

    klass.__lt__ = __lt__
    klass.__gt__ = __gt__
    klass.__le__ = __le__
    klass.__ge__ = __ge__
    klass.__eq__ = __eq__
    klass.__ne__ = __ne__
    return klass

#
# Versioning
#


@comparable
class _inf(object):
    """
    An object that is bigger than all other objects.
    """
    def __cmp__(self, other):
        """
        @param other: Another object.
        @type other: any

        @return: 0 if other is inf, 1 otherwise.
        @rtype: C{int}
        """
        if other is _inf:
            return 0
        return 1

_inf = _inf()


class IncomparableVersions(TypeError):
    """
    Two versions could not be compared.
    """


@comparable
class Version(object):
    """
    An object that represents a three-part version number.

    If running from an SVN/Git checkout, include the revision number/commit in
    the version string.
    """
    def __init__(self, package, major, minor, micro, prerelease=None):
        """
        @param package: Name of the package that this is a version of.
        @type package: C{str}
        @param major: The major version number.
        @type major: C{int}
        @param minor: The minor version number.
        @type minor: C{int}
        @param micro: The micro version number.
        @type micro: C{int}
        @param prerelease: The prerelease number.
        @type prerelease: C{int}
        """
        self.package = package
        self.major = major
        self.minor = minor
        self.micro = micro
        self.prerelease = prerelease

    def short(self):
        """
        Return a string in canonical short version format,
        <major>.<minor>.<micro>[+rSVNVer/@gitsha1].
        """
        s = self.base()
        gitver = self._getGitVersion()

        if not gitver:
            svnver = self._getSVNVersion()
            if svnver:
                s += '+r' + nativeString(svnver)

        else:
            s += '@' + gitver
        return s

    def base(self):
        """
        Like L{short}, but without the +rSVNVer or @gitsha1.
        """
        if self.prerelease is None:
            pre = ""
        else:
            pre = "pre%s" % (self.prerelease,)
        return '%d.%d.%d%s' % (self.major,
                               self.minor,
                               self.micro,
                               pre)

    def __repr__(self):
        svnver = self._formatSVNVersion()
        if svnver:
            svnver = '  #' + svnver
        if self.prerelease is None:
            prerelease = ""
        else:
            prerelease = ", prerelease=%r" % (self.prerelease,)
        return '%s(%r, %d, %d, %d%s)%s' % (
            self.__class__.__name__,
            self.package,
            self.major,
            self.minor,
            self.micro,
            prerelease,
            svnver)

    def __str__(self):
        return '[%s, version %s]' % (
            self.package,
            self.short())

    def __cmp__(self, other):
        """
        Compare two versions, considering major versions, minor versions, micro
        versions, then prereleases.

        A version with a prerelease is always less than a version without a
        prerelease. If both versions have prereleases, they will be included in
        the comparison.

        @param other: Another version.
        @type other: L{Version}

        @return: NotImplemented when the other object is not a Version, or one
            of -1, 0, or 1.

        @raise IncomparableVersions: when the package names of the versions
            differ.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented
        if self.package != other.package:
            raise IncomparableVersions("%r != %r"
                                       % (self.package, other.package))

        if self.prerelease is None:
            prerelease = _inf
        else:
            prerelease = self.prerelease

        if other.prerelease is None:
            otherpre = _inf
        else:
            otherpre = other.prerelease

        x = cmp((self.major,
                 self.minor,
                 self.micro,
                 prerelease),
                (other.major,
                 other.minor,
                 other.micro,
                 otherpre))
        return x

    def _parseGitDir(self, directory):

        headFile = os.path.abspath(os.path.join(directory, 'HEAD'))

        with open(headFile, "r") as f:
            headContent = f.read()

        if headContent.startswith("ref: "):
            with open(os.path.abspath(os.path.join(directory,
                                                   headContent[5:-1]))) as f:
                commit = f.read()
                return commit[:-1]

        return headContent

    def _getGitVersion(self):
        mod = sys.modules.get(self.package)
        if mod:
            basepath = os.path.dirname(mod.__file__)

            upOne = os.path.abspath(os.path.join(basepath, '..'))

            if ".git" in os.listdir(upOne):
                return self._parseGitDir(os.path.join(upOne, '.git'))

            while True:

                upOneMore = os.path.abspath(os.path.join(upOne, '..'))

                if upOneMore == upOne:
                    return None

                if ".git" in os.listdir(upOneMore):
                    return self._parseGitDir(os.path.join(upOneMore, '.git'))

                upOne = upOneMore

    def _parseSVNEntries_4(self, entriesFile):
        """
        Given a readable file object which represents a .svn/entries file in
        format version 4, return the revision as a string.  We do this by
        reading first XML element in the document that has a 'revision'
        attribute.
        """
        from xml.dom.minidom import parse
        doc = parse(entriesFile).documentElement
        for node in doc.childNodes:
            if hasattr(node, 'getAttribute'):
                rev = node.getAttribute('revision')
                if rev is not None:
                    return rev.encode('ascii')

    def _parseSVNEntries_8(self, entriesFile):
        """
        Given a readable file object which represents a .svn/entries file in
        format version 8, return the revision as a string.
        """
        entriesFile.readline()
        entriesFile.readline()
        entriesFile.readline()
        return entriesFile.readline().strip()

    # Add handlers for version 9 and 10 formats, which are the same as
    # version 8 as far as revision information is concerned.
    _parseSVNEntries_9 = _parseSVNEntries_8
    _parseSVNEntriesTenPlus = _parseSVNEntries_8

    def _getSVNVersion(self):
        """
        Figure out the SVN revision number based on the existence of
        <package>/.svn/entries, and its contents. This requires discovering the
        format version from the 'format' file and parsing the entries file
        accordingly.

        @return: None or string containing SVN Revision number.
        """
        mod = sys.modules.get(self.package)
        if mod:
            svn = os.path.join(os.path.dirname(mod.__file__), '.svn')
            if not os.path.exists(svn):
                # It's not an svn working copy
                return None

            formatFile = os.path.join(svn, 'format')
            if os.path.exists(formatFile):
                # It looks like a less-than-version-10 working copy.
                with open(formatFile, 'rb') as fObj:
                    format = fObj.read().strip()
                parser = getattr(self,
                                 '_parseSVNEntries_' + format.decode('ascii'),
                                 None)
            else:
                # It looks like a version-10-or-greater working copy, which
                # has version information in the entries file.
                parser = self._parseSVNEntriesTenPlus

            if parser is None:
                return b'Unknown'

            entriesFile = os.path.join(svn, 'entries')
            entries = open(entriesFile, 'rb')
            try:
                try:
                    return parser(entries)
                finally:
                    entries.close()
            except:
                return b'Unknown'

    def _formatSVNVersion(self):
        ver = self._getSVNVersion()
        if ver is None:
            return ''
        return ' (SVN r%s)' % (ver,)


def getVersionString(version):
    """
    Get a friendly string for the given version object.

    @param version: A L{Version} object.
    @return: A string containing the package and short version number.
    """
    result = '%s %s' % (version.package, version.short())
    return result


def _get_version(dist, keyword, value):
    """
    Get the version from the package listed in the Distribution.
    """
    if not value:
        return

    from distutils.command import build_py

    sp_command = build_py.build_py(dist)
    sp_command.finalize_options()

    for item in sp_command.find_all_modules():
        if item[1] == "_version":
            version_file = {}

            with open(item[2]) as f:
                exec(f.read(), version_file)

            dist.metadata.version = version_file["__version__"].short()
            return None

    raise Exception("No _version.py found.")


__version__ = Version("incremental", 15, 2, 0)

__all__ = ["__version__", "Version"]
