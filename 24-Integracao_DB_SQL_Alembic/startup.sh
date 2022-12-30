#!/bin/sh
#alembic init -t async migrations
#alembic revision --autogenerate -m "Adding User"

alembic upgrade head

uvicorn main:app --host 0.0.0.0 --port 8000