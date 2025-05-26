#!/usr/bin/env bash
set -o errexit  # Exit on error

pip install -r requirements.txt
python budget_tracker/manage.py migrate
python budget_tracker/manage.py loaddata categorySeed.json
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'user@example.com', 'user1234') if not User.objects.filter(username='user').exists() else None" | python budget_tracker/manage.py shell
python budget_tracker/manage.py collectstatic --no-input