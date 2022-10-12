#!/bin/bash

function error {
  echo "[error] $@" >&2
  exit 1
}
function info {
  echo "[info] $@" >&2
}

function invoke {
  info $@
  $@ || error "コマンドの実行に失敗しました"
}

function get_app_name {
  local app_name_path=$1
  cat $app_name_path | tr '[A-Z]' '[a-z]'
}

proxy="http://xxxxxxxxxx:7080"
no_proxy="169.254.169.254,169.254.170.2,10.0.0.0/8,localhost,127.0.0.1,.ap-northeast-1.amazonaws.com"