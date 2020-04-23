#!/usr/bin/env bash
sleep 10 # Wait for Postgres

# python manage.py db init
# python manage.py db migrate -m "Initial migration."
python manage.py db upgrade
