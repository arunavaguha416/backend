#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsu  # From your previous setup
python manage.py loaddata categorySeed.json  # Add this line