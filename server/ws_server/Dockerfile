FROM python:3.10.8
RUN apt-get update

WORKDIR /

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=C:/Windows/Temp \
    pip install -r requirements.txt

COPY . .

CMD [ "python", "ws_server.py"]