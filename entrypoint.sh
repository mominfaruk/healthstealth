#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e
python manage.py spectacular --file schema.yml
# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Start the application
echo "Starting the application"
printenv
exec "$@"
