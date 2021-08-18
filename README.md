## Development Setup

1. Install [poetry](https://github.com/python-poetry/poetry)
   ```bash
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
   ```
1. Install audio drivers if on server environment
   ```bash
   sudo apt install libasound2-dev
   ```
1. Install the dependencies
   ```bash
   poetry install
   ```
1. Install the [pre-commit](https://github.com/pre-commit/pre-commit) hooks
   ```bash
   pre-commit install
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
