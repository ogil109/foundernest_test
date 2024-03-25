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

# Decisions taken

## Data Quality

### Primary keys
amp_id seemed like an ID related to an event tracking platform (Amplitude?), but it wasn't unique. The event_time timestamp was unique, but it wouldn't have been a robust enough primary key if the event count per day scaled to a point where concurrency becomes a problem. Assuming a user couldn't generate various events at the same exact timestamp, a composite primary key consisting of user_id and event_time was chosen. Other candidate to compliment the timestamp was device_id, but to use it, I'd have had to assume that no device can have multiple active users and produce events concurrently (and it seemed more intuitive that a single user couldn't generate concurrent events).

### Data formatting
Light data formatting was made. Date was expressed as date, striping time attributes both for event and user signup date (in parse_json_date(json_date_str) helper). Hyphens were dynamically replaced for every JSON object for admin-dashboard-metabase and explore-companies (to align with class naming in case that dynamic updates for UserProperty attributes could be requested in the future).

### Duplicate handling
Duplicate handling was streamlined using class method checks before creating new instances of the ORM models.

### Nulls handling
Nulls in signup date are handled by the parse_json_date helper function, Nulls in the rest of the JSON objects are handled by the get dict method (defaulting to returning None).

## ORM with SQLAlchemy
ORM was used to build my tables declaratively and abstract SQL logic behing reusable tables. Besides that, I wanted to avoid redundancy by normalizing data and separating UserProperties from Event data, the decision to use ORM was justified in terms of avoiding redundancy, abstracting away SQL logic and documenting the models declaring them with classes. Each class also included a class method to check for instances using the primary key and avoid duplicates before creating new instances via parse_date_events().

## Transformations on raw SQL
For the transformations, however, it was more practical to stick to one-time CREATE and INSERT statements, relying in CTEs for the complex queries of user and corporate user statistics. Also, printing the query results to .TXTs in the Docker volume was a convenient way of displaying them as listed in the task requirements.

## Poetry and Docker
Poetry was used as dependency manager to build an exact poetry.lock file with dependencies' versions and use that file to build the docker image, representing a straightforward way of building only the required dependencies (poetry install --no-dev was passed by the dockerfile) in the specified app folder inside the container.

On the other side, a volume containing the database and the .TXTs results was setup at the same level as the app, to clearly present the results after interacting with the docker entrypoint, which was a bash terminal. This entrypoint was prefered to CMD even when forcing the user to manually run python run.py because the user could then have access to the load_date.py function.

# Software architecture

## Packaging

Packaging the app was a way to specify imports using absolute paths and build a clearer run.py separating the two main concerns of the challenge: to build the history table fetching data and to transform it to get the engagement metrics. The end-user can have a good general comprehension of these two areas by just looking at run.py.

## Session factory

The SQLAlchemy engine and session creation was exported to session_factory.py to avoid circular imports when initiating the app (an import from the models was necessary in order to build tables from the ORM classes).
