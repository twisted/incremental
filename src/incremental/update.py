import click

from incremental import Version
from datetime import date
from twisted.python.filepath import FilePath

_VERSIONPY_TEMPLATE = """# This file is auto-generated! Do not edit!
# Use `python -m incremental.update %s` to change this file.

from incremental import Version
version = %s

__all__ = ["__version__"]
"""

_YEAR_START = 2000


def _findPath(package):

    cwd = FilePath('.')

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


@click.command()
@click.argument('package')
@click.option('--path', default=None)
@click.option('--newversion', default=None)
@click.option('--patch', is_flag=True)
@click.option('--rc', is_flag=True)
@click.option('--dev', is_flag=True)
def _run(package, path, newversion, patch, rc, dev, _date=date.today()):

    if type(package) != str:
        package = package.encode('utf8')

    if not path:
        path = _findPath(package)
    else:
        path = FilePath(path)


    if newversion and patch or newversion and dev or newversion and rc:
        raise ValueError("Only give newversion")

    if dev and patch or dev and rc:
        raise ValueError("Only give dev")

    if newversion:
        pass
        # parse here

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
        v = Version(package, _date.year - _YEAR_START, _date.month, 0)


    if rc:
        v.release_candidate = (v.release_candidate or 0) + 1

    print("Updating %s/_version.py" % (path.path))

    version_repr = repr(v).split("#")[0]

    print(_VERSIONPY_TEMPLATE % (package, version_repr))

    return

    with path.child("_version.py").open('w') as f:
        f.write(_VERSIONPY_TEMPLATE % (package, version_repr))


if __name__ == '__main__':
    _run()
