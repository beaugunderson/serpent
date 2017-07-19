#!/bin/bash

set -e -x

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    "${PYBIN}/pip" install twine
    "${PYBIN}/pip" install -r /io/requirements-dev.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in /opt/python/*/bin/; do
    "${PYBIN}/pip" install ethereum-serpent-augur-temp --no-index -f /io/wheelhouse
    # (cd /io; "${PYBIN}/py.test")
    "${PYBIN}/twine" upload --skip-existing -u beaugunderson -p "$PYPI_PASSWORD" wheelhouse/*
done
