# syntax=docker/dockerfile:1.2

FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

WORKDIR /app/

# Env Vars
ENV POETRY_VERSION=1.2.0

# System deps:
RUN pip install "poetry==$POETRY_VERSION"
RUN poetry config virtualenvs.create false

# Install project with dev dependencies
COPY ./pyproject.toml ./poetry.lock* /app/
RUN poetry install --with dev  # TODO: different build for non-dev env

COPY ./src /app/src
