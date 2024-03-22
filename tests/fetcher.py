import json
from datetime import datetime, timedelta

import requests


def append_data_to_json(data, file_name="data_example.json"):
    """
    Appends data to a JSON file, maintaining a valid JSON structure.

    Args:
        data (dict): The data to append.
        file_name (str): The name of the JSON file.
    """
    try:
        # Try to read the existing data in the file
        try:
            with open(file_name, "r") as file:
                file_data = json.load(file)
        except FileNotFoundError:
            file_data = []

        # Append the new data
        file_data.append(data)

        # Write the updated data back to the file
        with open(file_name, "w") as file:
            json.dump(file_data, file, indent=4)

    except IOError as e:
        print(f"Error writing to file: {e}")


def get_date_events(date):
    """
    Retrieves user events for a given date and appends them to a JSON file,
    maintaining a valid JSON array structure.

    Args:
        date (str): The date for which to retrieve user events.
    """
    url = "http://35.212.243.98/user-events"
    headers = {"api-token": "BGjvhpFqkIFoBCvD0wwP"}
    params = {"date": date}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            # Create data structure to append
            data_to_append = {"date": date, "events": response.json()}
            append_data_to_json(data_to_append)
            print(f"Data for {date} retrieved and appended successfully.")
        else:
            print(
                f"Failed to retrieve data for {date}. Status code: {response.status_code}"
            )
    except requests.RequestException as e:
        print(f"Request failed for {date}: {e}")


def load_data() -> None:
    """
    Loads data from January and appends each day's data to a single JSON file,
    maintaining a valid JSON array structure.
    """
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)

    for dt in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=dt)
        get_date_events(date.strftime("%Y-%m-%d"))


load_data()
