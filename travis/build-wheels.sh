#!/bin/bash

set -e -x

yum install -y openssl openssl-devel

PYTHON_VERSIONS=( /opt/python/cp27-cp27m/bin /opt/python/cp27-cp27mu/bin /opt/python/cp36-cp36m/bin )

# Compile wheels
for PYBIN in "${PYTHON_VERSIONS[@]}"; do
    "${PYBIN}/pip" install -r /io/requirements-dev.txt
    "${PYBIN}/pip" wheel /io/ -w wheelhouse/
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install packages and test
for PYBIN in "${PYTHON_VERSIONS[@]}"; do
    "${PYBIN}/pip" install ethereum-serpent-augur-temp --no-index -f /io/wheelhouse
    # (cd /io; "${PYBIN}/py.test")
done

/opt/python/cp36-cp36m/bin/pip install twine
/opt/python/cp36-cp36m/bin/twine upload --skip-existing -u beaugunderson -p "$PYPI_PASSWORD" wheelhouse/*
