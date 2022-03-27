#!/bin/bash
SCRIPT_DIR=$(cd $(dirname $0); pwd)
source $SCRIPT_DIR/utils.sh

info MYSQL_PWD="$DB_PASSWORD" mysql -u "$DB_USER" -h "$DB_HOST" -P "$DB_PORT" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"
MYSQL_PWD="$DB_PASSWORD" mysql -u "$DB_USER" -h "$DB_HOST" -P "$DB_PORT" -e "CREATE DATABASE IF NOT EXISTS $DB_NAME;"