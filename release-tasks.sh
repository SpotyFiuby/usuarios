#!/bin/bash

poetry run alembic stamp head
poetry run alembic revision --autogenerate -m "New Migration"
poetry run alembic upgrade head