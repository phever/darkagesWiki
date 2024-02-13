#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..

if [[ $(git status --porcelain) ]]; then
  git pull
  systemctl restart gunicorn.service
  systemctl restart nginx.service
fi