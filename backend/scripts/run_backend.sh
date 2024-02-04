#!/bin/bash


./manage.py collectstatic --noinput
# Start Gunicorn processes
echo Starting Gunicorn.
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 1800 --graceful-timeout 1800
