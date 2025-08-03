#!/usr/bin/env bash

# Install dependencies
pip install -r requirements.txt

# Run Django migrations
python manage.py migrate

# Collect static files (optional, but good for production)
python manage.py collectstatic --noinput
