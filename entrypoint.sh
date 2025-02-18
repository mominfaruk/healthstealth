#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e
python manage.py spectacular --file schema.yml
# Collect static files
echo "Collecting static files"
python manage.py collectstatic --noinput


# Create superuser if not exists (using values from environment variables)
echo "Creating superuser—if it does not already exist"
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
email = "$SUPERUSER_EMAIL"
username = "$SUPERUSER_USERNAME"
password = "$SUPERUSER_PASSWORD"
if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, username=username, password=password)
    print("Superuser created")
else:
    print("Superuser already exists")
EOF

# Start the application
echo "Starting the application"
printenv
exec "$@"
