FROM python:slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt update && apt install -y binutils libproj-dev gdal-bin
WORKDIR /code
COPY ./Pipfile.lock /code
COPY ./Pipfile /code
RUN pip install pipenv; \
    pipenv install --system --deploy --ignore-pipfile