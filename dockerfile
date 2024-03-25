# Use the official Python image as the base image
FROM python:3.11.5-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install Poetry for dependency management
RUN pip install poetry

# Copy only the files needed for installing dependencies to leverage Docker cache
COPY poetry.lock pyproject.toml /app/

# Configure Poetry package
RUN poetry config virtualenvs.create false && poetry install --no-dev

# Copy the rest of the application code
COPY . /app

# Set an entrypoint for interactive mode
ENTRYPOINT ["/bin/bash"]
