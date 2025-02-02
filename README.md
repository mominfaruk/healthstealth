# HealthStealth Django Project

Welcome to the HealthStealth project! This repository contains a Django project configured to run using Docker, enabling you to easily set up an isolated development environment with all necessary services.

## Docker Configuration

The project uses Docker to containerize the application and its dependencies. The key configuration files include:

- **Dockerfile:** Builds the Django application image.
- **docker-compose.yml:** Defines the services needed for the complete stack, including:
    - Django Backend
    - PostgreSQL (Database)
    - Redis (Optional)
    - Elasticsearch (Optional)
    - Celery (Optional)

## Build and Run Containers

To start the entire stack, use docker-compose:

```bash
docker-compose up --build
```

This command will:

- Build the Django image using the Dockerfile.
- Install dependencies with pip.
- Collect static files using Django’s `collectstatic` command.
- Launch the application with Gunicorn listening on port 8080.

## Access the Application

Once the containers are running, open your browser and visit:

```
http://localhost:8080
```

## Common Commands

### Rebuild Containers
If you make changes to the Docker configuration or update dependencies, rebuild the containers:

```bash
docker-compose up --build
```

### Running Django Management Commands
To execute Django commands (e.g., applying migrations), run the following command inside the Django container:

```bash
docker-compose exec <service_name> python manage.py migrate
```

Replace `<service_name>` with the appropriate service name defined in your `docker-compose.yml` (commonly `web`).

## Troubleshooting

### Missing Environment Variables
Ensure that all required variables are defined in the `.env` file.

### Entrypoint Script
If you plan to use the `entrypoint.sh` script, verify it exists at the specified location and is correctly referenced in both `docker-compose.yml` and the Dockerfile.

### Static Files Issues
The Dockerfile automatically runs `collectstatic`. In case of any errors, double-check the Django settings and static files paths.

## Additional Information

- Review and adjust Django settings in `healthstealth/settings.py` as needed.
- Modify environment variables in the `.env` file.
- Update dependencies in `requirements.txt` and rebuild the Docker image if necessary.