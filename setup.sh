#!/bin/bash

set -e

[ -z $(which brew)  ] && /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
[ -z $(which python3)  ] && brew install python3
[ -z $(which direnv)  ] && brew install direnv
[ -z $(which virtualenv)  ] && python3 -m pip install virtualenv

echo "--------------------------------------"
echo "Paste mongodb connection string here:"
echo "--------------------------------------"
read mongo_conn_string
echo "export MONGO_DEV_URI='$mongo_conn_string'" > .envrc

if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

.venv/bin/pip install -r requirements.txt
direnv allow .
mkdir -p incoming_xlsx/trash
mkdir -p corrected_xlsx/trash

exit 0
