FROM python:3.10-alpine AS builder

# Install poetry
RUN pip install poetry

WORKDIR /app

# Copy config files
COPY poetry.lock pyproject.toml ./

# Install only dependencies
RUN poetry config virtualenvs.create false \
	&& poetry install

# Copy the app
COPY . ./

# Install packages
RUN poetry run pip install -e src/contexts

# Run the app
ENTRYPOINT poetry run uvicorn app:app --app-dir='src/apps/backend' --port 8000 --reload --host 0.0.0.0
