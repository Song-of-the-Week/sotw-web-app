#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
echo "Initializing database data"
python /app/db/init_db.py
python /app/main.py