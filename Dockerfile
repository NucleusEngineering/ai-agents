FROM debian:11-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev libpq-dev ffmpeg postgresql-client netcat && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel 

FROM build AS build-venv

COPY . /app

RUN /venv/bin/pip install --disable-pip-version-check -r /app/requirements.txt

ENV FLASK_APP main.py

WORKDIR /app

RUN mkdir -p /app/uploads

ENTRYPOINT ["./entrypoint.sh"]

