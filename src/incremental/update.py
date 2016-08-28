# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from __future__ import absolute_import, division

import click
import os

from incremental import Version
from datetime import date
from twisted.python.filepath import FilePath

_VERSIONPY_TEMPLATE = """# This file is auto-generated! Do not edit!
# Use `python -m incremental.update %s` to change this file.

from incremental import Version

__version__ = %s
__all__ = ["__version__"]
"""

_YEAR_START = 2000


def _findPath(path, package):

    cwd = FilePath(path)

    src_dir = cwd.child("src").child(package.lower())
    current_dir = cwd.child(package.lower())

    if src_dir.isdir():
        return src_dir
    elif current_dir.isdir():
        return current_dir
    else:
        raise ValueError(("Can't find under `./src` or `./`. Check the "
                          "package name is right (note that we expect your "
                          "package name to be lower cased), or pass it using "
                          "'--path'."))


def _existing_version(path):
    version_info = {}

    with path.child("_version.py").open('r') as f:
        exec(f.read(), version_info)

    return version_info["__version__"]


def _run(package, path, newversion, patch, rc, dev, create,
         _date=date.today(), _getcwd=os.getcwd):

    if type(package) != str:
        package = package.encode('utf8')

    update_NEXT = False

    if not path:
        path = _findPath(_getcwd(), package)
    else:
        path = FilePath(path)

    if newversion and patch or newversion and dev or newversion and rc:
        raise ValueError("Only give --newversion")

    if dev and patch or dev and rc:
        raise ValueError("Only give --dev")

    if create and dev or create and patch or create and rc or \
       create and newversion:
        raise ValueError("Only give --create")

    if newversion:
        existing = _existing_version(path)
        segments = newversion.split('.')

        v = Version(package, int(segments.pop(0)), int(segments.pop(0)),
                    int(segments.pop(0)))

        while segments:
            segment = segments.pop(0)

            if segment.startswith("dev"):
                v.dev = int(segment[3:])
            elif segment.startswith("rc"):
                v.release_candidate = int(segment[2:])
            elif segment.startswith("pre"):
                v.release_candidate = int(segment[3:])

    elif create:
        v = Version(package, _date.year - _YEAR_START, _date.month, 0)
        existing = v

    elif rc:
        existing = _existing_version(path)

        if existing.release_candidate:
            v = Version(package, existing.major, existing.minor,
                        existing.micro, (existing.release_candidate or 0) + 1)
        else:
            v = Version(package, _date.year - _YEAR_START, _date.month, 1)

    elif patch:
        existing = _existing_version(path)
        v = Version(package, existing.major, existing.minor,
                    existing.micro + 1)

    elif dev:
        existing = _existing_version(path)
        v = Version(package, existing.major, existing.minor,
                    existing.micro, existing.release_candidate,
                    dev=(existing.dev or 0) + 1)

    else:
        existing = _existing_version(path)

        if existing.release_candidate:
            v = Version(package, existing.major, existing.minor,
                        existing.micro, 0)
        else:
            raise ValueError("You need to issue a prerelease first!")

    if rc:
        v.release_candidate = (v.release_candidate or 0) + 1

    NEXT_repr = repr(Version(package, "NEXT", 0, 0)).split("#")[0]
    NEXT_repr_bytes = NEXT_repr.encode('utf8')

    version_repr = repr(v).split("#")[0]
    version_repr_bytes = version_repr.encode('utf8')

    existing_version_repr = repr(v).split("#")[0]
    existing_version_repr_bytes = existing_version_repr.encode('utf8')

    print("Updating codebase to %s" % (v.public()))

    for x in path.walk():

        if not x.isfile():
            continue

        original_content = x.getContent()
        content = original_content

        # Replace previous prerelease calls to the new one
        if existing.prerelease:
            content = content.replace(existing_version_repr_bytes,
                                      version_repr_bytes)

        # Replace NEXT Version calls with the new one
        content = content.replace(NEXT_repr_bytes,
                                  version_repr_bytes)
        content = content.replace(NEXT_repr_bytes.replace("'", '"'),
                                  version_repr_bytes)

        # Replace <package> NEXT with <package> <public>
        content = content.replace(package.lower().encode('utf8') + b" NEXT",
                                  v.public().encode('utf8'))

        if content != original_content:
            print("Updating %s" % (x.path,))
            with x.open('w') as f:
                f.write(content)

    print("Updating %s/_version.py" % (path.path))
    with path.child("_version.py").open('w') as f:
        f.write(_VERSIONPY_TEMPLATE % (package, version_repr))


@click.command()
@click.argument('package')
@click.option('--path', default=None)
@click.option('--newversion', default=None)
@click.option('--patch', is_flag=True)
@click.option('--rc', is_flag=True)
@click.option('--dev', is_flag=True)
@click.option('--create', is_flag=True)
def run(*args, **kwargs):
    return _run(*args, **kwargs)


if __name__ == '__main__':
    run()
