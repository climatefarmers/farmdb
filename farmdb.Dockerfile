FROM python:slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY ./Pipfile.lock /code
COPY ./Pipfile /code
RUN pip install pipenv; \
    pipenv install --system --deploy --ignore-pipfile
