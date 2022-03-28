#!/bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
PROJECT_ROOT=$(cd $SCRIPT_DIR/../../; pwd)
API_DIR=$(cd $SCRIPT_DIR/../../api; pwd)
source $SCRIPT_DIR/utils.sh

cd $API_DIR
invoke alembic downgrade base
invoke alembic upgrade head

cd $PROJECT_ROOT
invoke pytest api/test -s
