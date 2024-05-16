#!/bin/bash

echo "Building the project..."
python3.9 -m pip install -r requirements.txt
echo "Enter parfume project"
echo "Make Migration..."
python3.9 manage.py makemigrations --noinput
echo "Migrate..."
python3.9 manage.py migrate --noinput
echo "Collect Static..."
python3.9 manage.py collectstatic --noinput --clear

