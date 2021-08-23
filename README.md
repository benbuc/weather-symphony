# Weather Symphony

## Live Demo Website

LINK

### Docker

1. The Docker container for the live demo can be build with:
   ```bash
   $ docker build -t weather_symphony .
   ```
2. Then run it using:
   ```bash
   $ docker run -d -p 80:80 weather_symphony
   ```
3. Open the website (e.g. [http://localhost:80/](http://localhost:80/))

### Run Manually

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   $ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
2. Install audio drivers if on server environment
   ```bash
   $ sudo apt install libasound2-dev
   ```
3. Install the dependencies
   ```bash
   $ poetry install --no-dev
   ```
4. Run (add `--host 0.0.0.0` to bind to all addresses)
   ```bash
   $ poetry run uvicorn demo.main:app
   ```

## Run from command line

Perform steps 1. to 3. from the "Run Manually" chapter

4. Open the poetry shell
   ```bash
   $ poetry shell
   ```
5. `ws` runs Weather Symphony
   ```bash
   $ ws --help
   usage: ws [-h] [-d DATE] [-o OUTPUT]

   optional arguments:
   -h, --help            show this help message and exit
   -d DATE, --date DATE
   -o OUTPUT, --output OUTPUT
   ```

## Development Setup

Perform steps 1. and 2. from the "Run Manually" chapter

3. Install the dependencies
   ```bash
   $ poetry install
   ```
4. Install the [pre-commit](https://github.com/pre-commit/pre-commit) hooks
   ```bash
   $ pre-commit install
   ```
5. Run with uvicorn in development mode
   ```bash
   $ poetry run uvicorn demo.main:app --reload
   ```
