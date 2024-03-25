# Installation

Clone this repo locally:
git clone https://github.com/ogil109/foundernest_test.git

# Usage

## Add the API-TOKEN modifying docker-compose.yml
- Will set API-TOKEN as env variable to use it as header in the request to the endpoint.

## Execute:

### docker-compose run --rm app
- Will start a docker container, set up a workdir, install Poetry and use it to install production dependencies from poetry.lock.
- Will set an interactive bash entrypoint to run the application.

### python run.py
- Will execute the app, build the database for January 2024 and analyze requested data, outputing results to .TXTs in results folder (it will take a while).

### python load_date.py YYYY-MM-DD
- Will fetch all data for the given date in ISO 8601.
- Will save fetched data in the database (if not already present).