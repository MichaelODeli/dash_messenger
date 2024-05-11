FROM python:3.10.8
RUN apt-get update

WORKDIR /

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=C:/Windows/Temp \
    pip install -r requirements.txt

COPY . .

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

CMD [ "python", "ws_server.py"]