# Usage
	- ## docker-compose run --rm app
		- Will start a docker container, set up a workdir, install Poetry and use it to install production dependencies.
		- Will set an interactive bash entrypoint.
	- ## python run.py
		- Will call the app, build the database for January 2024 and analyze requested data, outputing results to .TXT in results folder.
	- ## python load_date.py YYYY-MM-DD
		- Will fetch all data for the given date in ISO 8601.