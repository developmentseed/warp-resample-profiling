#!/bin/bash

set -xe

SOURCE_DIR="${SOURCE_DIR:-${HOME}/source}"
STACK_DIR="${STACK_DIR:-${HOME}/stack}"
ESMF_VERSION="8.7.0"
ESMF_URL="https://github.com/esmf-org/esmf/archive/refs/tags/v${ESMF_VERSION}.tar.gz"
export ESMF_DIR="${SOURCE_DIR}/esmf-${ESMF_VERSION}"
export ESMF_INSTALL_PREFIX="${STACK_DIR}/esmf-${ESMF_VERSION}"

mkdir -p ${SOURCE_DIR}
mkdir -p ${STACK_DIR}
mkdir -p ${ESMF_DIR}

cd ${ESMF_DIR}

curl -L ${ESMF_URL} | tar --strip-components=1 -xz

make all install

# this is an unused dumping grounds and causes disconcerting warnings
cd ${ESMF_DIR}/src/addon/esmpy
rm -rf src/esmpy/fragments

export ESMFMKFILE="${ESMF_INSTALL_PREFIX}/lib/esmf.mk"

python -m pip install .

chown -R ${USER}:${USER} ${ESMF_INSTALL_PREFIX}

cd ${SOURCE_DIR} && rm -rf ${ESMF_DIR}

export PATH="${PATH}:${ESMF_INSTALL_PREFIX}/bin"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${ESMF_INSTALL_PREFIX}/lib"
