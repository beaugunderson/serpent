#!/bin/bash

set -e -x

# Install a system package required by our library
yum install -y openssl openssl-devel

# Compile wheels
for PYBIN in /opt/python/*/bin; do
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
    (cd "$HOME"; "${PYBIN}/py.test")
done
