# Update the version, tag a release, and trigger the GHA release workflow
release:
    #!/bin/bash
    set -exu -o pipefail
    # TODO: Replace `tox` with `uv run`
    tox -e release --notest
    if [[ $(git rev-parse --abbrev-ref HEAD) != trunk ]]
    then
        echo "ERROR: Must be on trunk branch"
        exit 1
    fi
    if ! git diff --quiet HEAD
    then
        echo "ERROR: Dirty working copy"
        exit 1
    fi
    # Incremental doesn't do release candidates.
    .tox/release/bin/incremental update Incremental --rc
    .tox/release/bin/incremental update Incremental
    version=$(.tox/release/bin/hatch version)
    tag="incremental-$version"
    .tox/release/bin/towncrier build --yes
    git add -A NEWS.rst src/incremental/newsfragments src/incremental/_version.py
    git commit -m "Release $version"
    git tag "$tag"
    git push origin "$tag"
    git push origin trunk
