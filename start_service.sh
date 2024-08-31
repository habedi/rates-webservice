#!/bin/bash

# Loading environment variables
if source .env; then
    echo "Environment variables loaded successfully. :)"
else
    echo "Failed to load environment variables from .env file. :(" >&2
    exit 1
fi

echo "Starting the web service using Gunicorn (WSGI) HTTP server"
if poetry run gunicorn --timeout "$GUNICORN_TIMEOUT" --log-level "$GUNOCORN_LOG_LEVEL" -w "$GUNICORN_NUM_WOKERS" \
          -b "$GUNICORN_HOST:$GUNICORN_PORT" "$FLASK_APP"; then
    echo "Service started successfully."
else
    echo "Failed to start the service." >&2
    exit 1
fi