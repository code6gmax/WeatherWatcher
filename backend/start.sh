#!/bin/sh

# Run Database Migrations (Optional here since we used create_all in main.py, 
# but good practice for future)

# Start the Gunicorn Server
exec gunicorn -k uvicorn.workers.UvicornWorker -w 1 -b 0.0.0.0:8000 main:app