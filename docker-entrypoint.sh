#!/bin/bash

echo "Applying DB INIT"
python manage.py db init

echo "Applying DB MIGRATE"
python manage.py db migrate

echo "Applying DB UPGRADE"
python manage.py db upgrade

echo "Starting server"
python server.py