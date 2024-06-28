FROM python:3.12.3-slim
LABEL maintainer="saru.com"


ENV PYTHONUNBUFFERED 1


COPY ./docker_requirements.txt /docker_requirements.txt
COPY ./webapp /webapp
COPY ./models/models.joblib /models/models.joblib

WORKDIR /webapp
EXPOSE 8000   


RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /docker_requirements.txt && \
    adduser --disabled-password --no-create-home webapp
    #adding webapp as an user

ENV PATH="/py/bin:$PATH"

USER webapp