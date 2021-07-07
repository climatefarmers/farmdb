FROM python:slim-buster
RUN apt-get update && apt-get install -y git curl autoconf automake libtool python-dev pkg-config build-essential

RUN cd /usr/local && git clone https://github.com/openvenues/libpostal

# Create Libpostal data directory at /var/libpostal/data
RUN cd /var && \
	mkdir libpostal && \
	cd libpostal && \
	mkdir data

# Install Libpostal from source
RUN cd /usr/local/libpostal && \
    ./bootstrap.sh && \
    ./configure --datadir=/var/libpostal/data && \
    make -j4 && \
    make install && \
    ldconfig


WORKDIR /code
COPY ./Pipfile.lock /code
COPY ./Pipfile /code
RUN pip3 install pipenv; \
    pipenv install --system --deploy
COPY ./main.py /code/

# Compile to pyc for faster startup
RUN python -m compileall .

ENTRYPOINT ["uvicorn"]
CMD ["main:app", "--host", "0.0.0.0"]
