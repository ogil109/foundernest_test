import json

import requests


def get_user_events(date):
    url = "http://35.212.243.98/user-events"
    headers = {"api-token": "BGjvhpFqkIFoBCvD0wwP"}
    params = {"date": date}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(response.status_code)


get_user_events("2024-01-02")
