FROM python:3.11-slim-buster

RUN pip install poetry==1.4.2
    
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1


WORKDIR /app
# install system dependencies
RUN apt-get update \
  && apt-get -y install libpq-dev gcc 


COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN poetry install --without dev --no-root

COPY . .


