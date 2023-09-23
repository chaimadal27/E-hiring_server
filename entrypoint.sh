#!/bin/bash

set -e

echo -e "Running $DJANGO_ENV Env\n*****************\n"

if [[ $DJANGO_RUN_MIGRATION = "on" ]]; then
  echo -e "Wait for database to start : Waiting \n"
  exec sleep 10 &
  wait $!
  echo -e "Run migrations : Start \n"
  echo -e "Default database migrations : Start \n"
  exec python3 src/manage.py migrate jwt_authentication --database=default&
  wait $!
  echo -e "Default database migrations : End \n"
  echo -e "Dev database migrations : Start \n"
  exec python3 src/manage.py migrate --database "$POSTGRES_DB_DEV" &
  wait $!
  echo -e "Dev database migrations : End \n"
  echo -e "Run migrations : Done \n"
  exec python3 src/manage.py create_admin -u admin -e admin@admin.com  -w admin -d "$POSTGRES_DB_DEV" -c 1 -P 23125852 -f admin  -F admin  -l admin  -L admin &
  wait $!
  echo -e "Run Create Groups : Start \n"
  exec python3 src/manage.py create_groups --database "$POSTGRES_DB_DEV" &
  wait $!
  # exec python3 src/manage.py timeSheetManagement --database "$POSTGRES_DB_DEV" &
  # wait $!
  echo -e "Run Create Groups : End \n"
fi

if [[ $DJANGO_ENV = "development" ]]; then
  echo -e "Starting development server\n***********\n"
  exec python3 src/manage.py runserver 0.0.0.0:5000
  #exec uwsgi --ini src/config/uwsgi.ini --py-autoreload=1 --cheaper=N
elif [[ $DJANGO_ENV = "testing" ]]; then
  echo -e "Running tests\n************\n"
  exec python3 src/manage.py  tests
elif [[ $DJANGO_ENV = "production" ]]; then
  echo -e "Starting production server\n************\n"
  exec uwsgi --ini src/config/uwsgi.ini
else
  echo -e "Invalid config $DJANGO_ENV"
fi
