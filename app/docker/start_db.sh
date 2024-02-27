#!/bin/bash

echo "Building database '$(DB_NAME)'"
echo "CREATE USER $(DB_DEV_USER) WITH PASSWORD '$(DB_DEV_PASS)'" | psql -d postgres
echo "CREATE DATABASE $(DB_NAME) WITH OWNER $(DB_DEV_USER) ENCODING 'UTF8'" | psql -d postgres
echo "CREATE DATABASE $(DB_TEST_NAME) WITH OWNER $(DB_DEV_USER) ENCODING 'UTF8'" | psql -d postgres