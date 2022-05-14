FROM python:3.9.12

WORKDIR /app

ENV POETRY_VERSION=1.1.13

# Install Python env
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false
COPY ./pyproject.toml /app/
COPY ./poetry.lock /app/
RUN poetry install

COPY . /app

CMD ["poetry", "run", "uvicorn", "app.main:app", "--log-level", "debug", "--reload", "--host", "0.0.0.0", "--port", "8080"]