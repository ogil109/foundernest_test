import json
from datetime import datetime

import requests

from app import session
from app.database.models import Event, EventMetadata, UserProperties


def get_date_events(date) -> json.Any | None:
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
        parse_date_events(response.json())
    print(response.status_code)


def parse_json_date(json_date_str) -> datetime:
    # Helper function to parse JSON date strings
    return datetime.strptime(json_date_str, "%Y-%m-%dT%H:%M:%SZ")


def parse_date_events(events_data) -> None:
    """
    Parses events from JSON data and creates Event, EventMetadata, and UserProperties instances.

    Args:
        events_data (json): The JSON response containing the user events for a given date.
    """

    for event in events_data:
        # Create an Event instance for each object in JSON data
        event = Event(
            # Event ID
            amp_id=events_data.get("amp_id"),
            # Origin
            user_id=events_data.get("user_id"),
            device_id=events_data.get("device_id"),
            app=events_data.get("app"),
            # Time
            date=parse_json_date(events_data.get("date")),
            event_time=events_data.get("event_time"),
            client_event_time=events_data.get("client_event_time"),
            client_upload_time=events_data.get("client_upload_time"),
            processed_time=events_data.get("processed_time"),
            server_upload_time=events_data.get("server_upload_time"),
            server_received_time=events_data.get("server_received_time"),
            # Location
            country=events_data.get("country"),
            region=events_data.get("region"),
            city=events_data.get("city"),
            language=events_data.get("language"),
        )

        # Add the Event instance to the session
        session.add(event)

        event_metadata = EventMetadata(
            amp_id=events_data.get("amp_id"),
            # Event metadata
            data_type=events_data.get("data_type"),
            event_type=events_data.get("event_type"),
            data=json.dumps(events_data.get("data")),
        )

        # Add the EventMetadata instance to the session
        session.add(event_metadata)

        # Checking for UserProperties already in the database
        existing_user_properties = (
            session.query(UserProperties)
            .filter_by(user_id=events_data.get("user_id"))
            .first()
        )

        if existing_user_properties:
            pass
        else:
            user_properties = UserProperties(
                # User ID
                user_id=events_data.get("user_id"),
                # User properties
                admin_dashboard_metabase=events_data.get("admin_dashboard_metabase"),
                explore=events_data.get("explore"),
                explore_companies=events_data.get("explore_companies"),
                explore_prompt_validation=events_data.get("explore_prompt_validation"),
                initial_li_fat_id=events_data.get("initial_li_fat_id"),
                initial_rtd_cid=events_data.get("initial_rtd_cid"),
                subspaces=events_data.get("subspaces"),
                user_corporate_id=events_data.get("user_corporate_id"),
            )

            # Add the UserProperties instance to the session
            session.add(user_properties)

        # Commit the session to save the event to the database
        try:
            session.commit()
        except Exception as e:
            print(f"An error occurred ({e}) saving event: {event.amp_id}")
            session.rollback()
