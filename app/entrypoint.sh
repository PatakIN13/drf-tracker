#!/bin/sh

python manage.py migrate
python manage.py initadmin

exec "$@"