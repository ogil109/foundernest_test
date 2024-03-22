import json
from datetime import datetime
from typing import Any

import requests

from app.database.models import Event, EventMetadata, UserProperties
from app.database.session_factory import get_session


def get_date_events(date) -> Any:
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
    session = get_session()
    for event_data in events_data:
        # Create an Event instance for each object in JSON data
        event = Event(
            # Event ID
            amp_id=event_data.get("amp_id"),
            # Origin
            user_id=event_data.get("user_id"),
            device_id=event_data.get("device_id"),
            app=event_data.get("app"),
            # Time
            date=parse_json_date(event_data.get("date")),
            event_time=event_data.get("event_time"),
            client_event_time=event_data.get("client_event_time"),
            client_upload_time=event_data.get("client_upload_time"),
            processed_time=event_data.get("processed_time"),
            server_upload_time=event_data.get("server_upload_time"),
            server_received_time=event_data.get("server_received_time"),
            # Location
            country=event_data.get("country"),
            region=event_data.get("region"),
            city=event_data.get("city"),
            language=event_data.get("language"),
        )

        # Add the Event instance to the session
        session.add(event)

        event_metadata = EventMetadata(
            amp_id=event_data.get("amp_id"),
            # Event metadata
            data_type=event_data.get("data_type"),
            event_type=event_data.get("event_type"),
            data=json.dumps(event_data.get("data")),
        )

        # Add the EventMetadata instance to the session
        session.add(event_metadata)

        # Check if the UserProperties instance already exists from another event, if not, create it
        if not (
            existing_user_properties := UserProperties.get_by_user_id(
                session, event_data.get("user_id")
            )
        ):
            user_properties = UserProperties(
                # User ID
                user_id=event_data.get("user_id"),
                # User properties
                admin_dashboard_metabase=event_data.get("admin_dashboard_metabase"),
                explore=event_data.get("explore"),
                explore_companies=event_data.get("explore_companies"),
                explore_prompt_validation=event_data.get("explore_prompt_validation"),
                initial_li_fat_id=event_data.get("initial_li_fat_id"),
                initial_rtd_cid=event_data.get("initial_rtd_cid"),
                subspaces=event_data.get("subspaces"),
                user_corporate_id=event_data.get("user_corporate_id"),
            )

            # Add the UserProperties instance to the session
            session.add(user_properties)

        # Commit the session to save the instances to the database (for every event for debugging)
        try:
            session.commit()
        except Exception as e:
            print(f"An error occurred ({e}) saving event: {event.amp_id}")
            session.rollback()

    session.close()
