# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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

