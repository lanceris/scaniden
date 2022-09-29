#!/bin/sh

while ! nc -z mysql 3306; do sleep 1; done;

alembic upgrade head
python data_loader.py &
uvicorn app.main:app --host 0.0.0.0 --port 8000