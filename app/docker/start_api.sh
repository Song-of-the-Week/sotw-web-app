#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

cd /
alembic upgrade head
echo "Initializing database data"
python /usr/src/app/db/init_db.py
echo "Starting backend"
python /usr/src/app/main.py