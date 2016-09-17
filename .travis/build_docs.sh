#!/bin/bash

if [[ ${TRAVIS_PULL_REQUEST} == "false" ]] && [[ ${TRAVIS_BRANCH} == "master" ]]; then

    echo "uploading docs"

    REV=`git rev-parse HEAD`

    # Build the docs
    tox -e apidocs

    # Make the directory
    git clone --branch gh-pages https://github.com/hawkowl/incremental.git /tmp/tmp-docs

    # Copy the docs
    rsync -rt --del --exclude=".git" apidocs/* /tmp/tmp-docs/docs/

    cd /tmp/tmp-docs

    git add -A

    # set the username and email. The secure line in travis.yml that sets
    # these environment variables is created by:

    # travis encrypt 'GIT_NAME="HawkOwl (Automatic)" GIT_EMAIL=hawkowl@atleastfornow.net GH_TOKEN=<token>'

    export GIT_COMMITTER_NAME="${GIT_NAME}";
    export GIT_COMMITTER_EMAIL="${GIT_EMAIL}";
    export GIT_AUTHOR_NAME="${GIT_NAME}";
    export GIT_AUTHOR_EMAIL="${GIT_EMAIL}";

    git commit -m "Built from ${REV}";

    # Push it up
    git push -q "https://${GH_TOKEN}@github.com/hawkowl/incremental.git" gh-pages
else
    echo "skipping docs upload"
fi;
