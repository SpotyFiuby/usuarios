#!/bin/bash
echo "stamp"
poetry run alembic stamp head
echo "revision"
poetry run alembic revision --autogenerate -m "New Migration"
echo "update"
poetry run alembic upgrade head