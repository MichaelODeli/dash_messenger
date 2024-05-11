FROM python:3.10.8
RUN apt-get update

WORKDIR /app

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=C:/Windows/Temp \
    pip install -r requirements.txt

COPY . .

# CMD [ "python", "app.py"]
CMD [ "python", "server/ws_server/ws_server_tests.py"]