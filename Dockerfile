FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=healthstealth.settings


RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git-core \
        build-essential \
        binutils \
        libproj-dev \
        gdal-bin \
        supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN mkdir -p /app/media
WORKDIR /app
ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080

RUN mkdir -p /var/logs/app

COPY . /app


RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--workers", "4", "--timeout", "120", "--bind", "0.0.0.0:8080", "healthstealth.wsgi:application"]
