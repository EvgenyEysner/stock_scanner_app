#!/bin/bash
echo "django shell commands for local execution"

python ./manage.py migrate  # Apply database migrations

echo "Starting django server on https://192.168.178.25:8000/"
exec python manage.py runsslserver 192.168.178.25:8000
