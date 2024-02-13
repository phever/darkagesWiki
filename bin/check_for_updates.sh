#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd $SCRIPT_DIR/..

same_commit(){
    set -- $(git show-ref --hash --verify "$@")
    [ "$1" = "$2" ]
}
# get the changes if any, but don't merge them yet
git fetch origin
# See if there are any changes
if same_commit mainline origin/mainline
then
   echo "Everything up to date"
   exit 0
fi
# Now merge the remote changes
git pull
venv/bin/python manage.py migrate
systemctl restart gunicorn.service
systemctl restart nginx.service
