#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
API_DIR=$(cd $SCRIPT_DIR/../../api; pwd)
source $SCRIPT_DIR/utils.sh
cd $API_DIR

invoke alembic $*
