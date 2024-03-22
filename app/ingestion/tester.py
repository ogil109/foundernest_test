import json

import requests


def get_date_events(date):
    """
    Retrieves user events for a given date.

    Args:
        date (str): The date for which to retrieve user events.

    Returns:
        json.Any | None: The JSON response containing the user events, or None if the request fails.
    """
    url = "http://35.212.243.98/user-events"
    headers = {"api-token": "BGjvhpFqkIFoBCvD0wwP"}
    params = {"date": date}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code == 200:
        file = "data_example.json"
        with open(file, "w") as f:
            json.dump(response.json(), f, indent=4)
    print(response.status_code)


get_date_events("2024-01-03")
