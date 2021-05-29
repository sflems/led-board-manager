#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}/.."
./env/bin/gunicorn Capstone.wsgi -b 0:9002

exit 0