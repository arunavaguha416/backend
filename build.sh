#!/usr/bin/env bash

# Exit on any error
set -o errexit

# Debug: Print current working directory
echo "Current working directory: $(pwd)"

# Step 1: Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install --no-cache-dir -r requirements.txt

# Step 2: Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Step 3: Run migrations
echo "Running migrations..."
python manage.py migrate

# Step 4: Create superuser
echo "Creating superuser..."
python manage.py createsu

# Step 5: Load categorySeed.json
echo "Loading categorySeed.json..."
python manage.py loaddata categorySeed.json

# Debug: Confirm completion
echo "Build completed successfully."