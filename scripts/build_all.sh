#!/bin/bash

RED='\033[1;91m'
GREEN='\033[1;92m'
BLUE='\033[1;94m'
NC='\033[0m' # No Color

SCRIPT_DIR="$( cd "$(dirname "$0")" ; pwd -P )"
BASE_DIR=${SCRIPT_DIR}/..
THIRD_PARTY_DIR=${BASE_DIR}/third_party
EPICS_BASE_DIR=${THIRD_PARTY_DIR}/epics-base
PVXS_DIR=${THIRD_PARTY_DIR}/pvxs
NCPUS=4

# A simple function to check if an error occurred while building
trycmd(){
    "$@"
    local status=$?
    if [ $status -ne 0 ]; then
        echo -e "${RED}Error occurred with $1 ${NC}" >&2
        exit $status
    fi
    return $status
}

checkresult(){
    local status=$?
    if [ $status -ne 0 ]; then
        if [ ${LOG_FILE_NAME+x} ]
        then
            echo -e "${RED}FAILED. See log " ${LOG_FILE_NAME} " for details. Exiting...${NC}"
        else
            echo -e "${RED}FAILED. Last command failed. Exiting...${NC}"
        fi
        exit $status
    fi
}

clean(){
    trycmd cd ${BASE_DIR}
    trycmd make clean uninstall
    checkresult
}

build_base(){
    trycmd cd ${BASE_DIR}
    trycmd make clean uninstall -C ${EPICS_BASE_DIR}
    trycmd make -C ${EPICS_BASE_DIR}
    checkresult
}

build_pvxs(){
    trycmd cd ${BASE_DIR}
    cat <<EOF > $PVXS_DIR/configure/RELEASE.local
EPICS_BASE=$EPICS_BASE_DIR
EOF
    checkresult
    trycmd make clean uninstall -C ${PVXS_DIR}
    trycmd make -C ${PVXS_DIR}
    checkresult
}

build_this(){
    trycmd cd ${BASE_DIR}
    cat <<EOF > $BASE_DIR/configure/RELEASE.local
PVXS=$PVXS_DIR
EPICS_BASE=$EPICS_BASE_DIR
EOF
    checkresult
    trycmd make -j${NCPUS}
    checkresult
}

clean
build_base
build_pvxs
build_this