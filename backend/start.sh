#!/bin/bash

# 1. Start Celery Worker & Beat in the background
# The '&' symbol tells Linux to run this in the background so it doesn't block the API
celery -A tasks worker --beat --loglevel=info &

# 2. Start the FastAPI Server (Foreground)
# We use the $PORT environment variable which Render provides automatically
exec gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:$PORT main:app
