# Weather Symphony

We want to generate a 2 minute artistic rendition of a days weather events and convey it’s feelings. Using weather APIs, we strive to compose performable orchestral pieces valuing aesthetics over interpretability.

## Live Demo Website

https://weathersymphony.benbuc.de

To ease experimentation, we've set up a little demo website which runs a small webform to run the Weather Symphony generator. All you have to do is to request a personal access token for the weather API we are using.
Using the link above you can access an instance of this interface to play around with. In case you want to host it yourself you can look at the following chapters which will guide you through the setup process.

### Docker

We created a little Dockerfile to ease the setup of this project. After cloning the repository you can use the following steps to build and run the container.

1. The Docker container for the live demo can be build with:
   ```bash
   docker build -t weather_symphony .
   ```
2. Then run it using:
   ```bash
   docker run -d -p 80:80 --name weather_symphony weather_symphony
   ```
3. Open the website (e.g. [http://localhost:80/](http://localhost:80/))

### Run Manually

If you prefer to run the project manually instead of using Docker you can use the following steps after cloning the repository.

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
2. Install audio drivers if on server environment
   ```bash
   sudo apt install libasound2-dev
   ```
3. Install the dependencies
   ```bash
   poetry install --no-dev
   ```
4. Run (add `--host 0.0.0.0` to bind to all addresses)
   ```bash
   poetry run uvicorn demo.main:app
   ```

## Run from command line

Aside using the simple web interface, you can also run the Weater Symphony generator directly from the command line. Use the following guide on how to interact with the generator.

Perform steps 1. to 3. from the "Run Manually" chapter

4. Open the poetry shell
   ```bash
   poetry shell
   ```
5. `ws` runs Weather Symphony
   ```bash
   $ ws --help
   usage: ws [-h] -i INPUT -o OUTPUT [-s SEED]

   optional arguments:
   -h, --help            show this help message and exit
   -i INPUT, --input INPUT
   -o OUTPUT, --output OUTPUT
   -s SEED, --seed SEED
   ```

When running the generator, you have mutliple parameters to hand over to the program.
You need to specify the input `json` or `yaml` file. Look at the `weather_data/` directory for some sample files.
The output parameters specifies the filepath to where the final MIDI-File is saved to.
Optionally, you can also specify a seed which is used for the random generator. This way, the output symphony for a constant inpute file will be different.

## Development Setup

The following steps can be used to set up the development environment using all the dev dependencies and pre-commit hooks.

Perform steps 1. and 2. from the "Run Manually" chapter

3. Install the dependencies
   ```bash
   poetry install
   ```
4. Install the [pre-commit](https://github.com/pre-commit/pre-commit) hooks
   ```bash
   pre-commit install
   ```
5. Run with uvicorn in development mode
   ```bash
   poetry run uvicorn demo.main:app --reload
   ```
