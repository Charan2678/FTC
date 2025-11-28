#!/usr/bin/env bash
# Start script for Render deployment

# Get the PORT from environment variable (Render provides this)
PORT=${PORT:-10000}

# Start Gunicorn with the correct WSGI application
exec gunicorn FTC.wsgi:application \
    --bind 0.0.0.0:$PORT \
    --workers 3 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
