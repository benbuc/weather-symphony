# Development Setup

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

# Run

Install poetry like in development setup, then:

```bash
poetry run uvicorn demo.main:app
```

# Docker

The Docker container can be build with:

```bash
docker build -t weather_symphony .
```

Then run it using:

```bash
docker run -d -p 80:80 weather_symphony
```

# Scenes

- overcast
  - thunderstorm
  - intense_rain
  - rainy (drizzle)
    - hot
    - cold
  - windy
- broken
  - misty
  - gusty
  - rainy
  - rainbow
  - approaching
- scattered (\< 50% clouds)
  - clearing
  - shower
  - light_precipitation
  - windy
  - hot
  - sweltry
- clear (sunny, \< 15% clouds)
  - broiling
  - sweltry
  - nice
  - hazy
  - chilly
- night
  - chilly
  - warm
  - thunderstorm
  - stormy

https://openweathermap.org/weather-conditions#Weather-Condition-Codes-2
