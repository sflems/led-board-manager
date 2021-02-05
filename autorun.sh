#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "${DIR}/.."

python3 ${DIR}/manage.py runserver 0:9002 --noreload &

exit 0