#!/bin/bash

while :; do
  success=$(MYSQL_PWD=$DB_PASSWORD mysql -u $DB_USER -h 127.0.0.1 $DB_NAME -e "SELECT 'success'" >/dev/null 2>&1; echo $?)
  if [ "$success" = "0" ]; then
    echo "success!!"
    break
  else
    echo "mysql booting..."
  fi
  sleep 1
done