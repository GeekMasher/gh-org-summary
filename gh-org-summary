#!/bin/bash
set -eu

export EXTENSION_LOCATION="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

pushd $EXTENSION_LOCATION > /dev/null

if [ ! -z ${1+x} ]; then
    if [ "$1" = "install" ]; then
        pip install pipenv
        pipenv install --system

        echo "Installed dependencies!"
        exit 0
    fi
fi

python3 $EXTENSION_LOCATION/summary.py $@

popd > /dev/null
