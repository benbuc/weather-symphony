# syntax = docker/dockerfile:1.2
FROM python:latest

RUN apt update; apt install -y libasound2-dev libjack-dev
RUN apt install -y fluid-soundfont-gm fluidsynth
RUN apt install -y ffmpeg

EXPOSE 80
WORKDIR /app

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false
ENV PATH="/opt/poetry/bin:/opt/poetry/venv/bin/:${PATH}"

COPY ./pyproject.toml ./poetry.lock README.md ./
RUN --mount=type=cache,target=/root/.cache poetry install --no-root --no-dev --no-interaction --no-ansi
RUN pip install virtualenv
COPY ./weather_symphony ./weather_symphony
COPY ./demo ./demo
RUN --mount=type=cache,target=/root/.cache poetry install --no-dev --no-interaction --no-ansi

CMD ["uvicorn", "demo.main:app", "--host", "0.0.0.0", "--port", "80"]
