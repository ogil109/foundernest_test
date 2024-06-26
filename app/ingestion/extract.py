import json
import os
from datetime import date, datetime

import requests

from app.database.models import Event, EventMetadata
from app.database.session_factory import get_session


def get_date_events(events_date) -> bool | None:
    url = "http://35.212.243.98/user-events"
    headers = {"api-token": os.getenv("API_TOKEN")}
    params = {"date": events_date}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    if response.status_code == 200:
        return bool(
            parse_date_events(response.json())
        )  # Will return False if there are no events


def parse_json_date(json_date_str) -> date | None:
    """
    Helper to parse the given JSON date string to a date object, handling ISO 8601 with and without mss. Return the date object (after strp time attributes).
    """
    if json_date_str is not None:
        try:
            # Handling both ISO 8601 with and without milliseconds (signups and event dates)
            dt = datetime.fromisoformat(json_date_str)
            # Return date object strictly (strp time attributes)
            return dt.date()
        except ValueError:
            return None

    # Handle missing values (in signup date)
    return None


def parse_date_events(events_data) -> bool:
    """
    Parses the events data and saves the event instances to the database.

    Args:
        events_data: A list of event data for a given date containing information such as event_time, user_id, user_properties, and event metadata.

    Returns:
        bool: True if any event instance is committed, False otherwise.
    """
    session = get_session()

    # Default value for events saved (will be set to True if any event instance is committed)
    events_saved = False

    for event_data in events_data:
        # Handle event duplicates (same event_time and user_id)
        if not Event.get_by_event_time_and_user_id(
            session, event_data.get("event_time"), event_data.get("user_id")
        ):
            # Create a dictionary of user properties for retrieval
            user_properties_data = {
                key.replace("-", "_"): value
                for key, value in event_data.get("user_properties").items()
            }

            # Create an Event instance for each unique object in JSON data
            event = Event(
                # Event ID
                event_time=event_data.get("event_time"),
                user_id=event_data.get("user_id"),
                # Origin
                amp_id=event_data.get("amp_id"),
                device_id=event_data.get("device_id"),
                app=event_data.get("app"),
                date=parse_json_date(event_data.get("date")),
                # Location
                country=event_data.get("country"),
                region=event_data.get("region"),
                city=event_data.get("city"),
                language=event_data.get("language"),
                # User properties
                admin_dashboard_metabase=user_properties_data.get(
                    "admin_dashboard_metabase"
                ),
                explore=user_properties_data.get("explore"),
                explore_companies=user_properties_data.get("explore_companies"),
                explore_prompt_validation=user_properties_data.get(
                    "explore_prompt_validation"
                ),
                initial_li_fat_id=user_properties_data.get("initial_li_fat_id"),
                initial_rtd_cid=user_properties_data.get("initial_rtd_cid"),
                subspaces=user_properties_data.get("subspaces"),
                user_corporate_id=user_properties_data.get("user_corporate_id"),
                user_corporate_is_demo=user_properties_data.get(
                    "user_corporate_is_demo"
                ),
                user_corporate_status=user_properties_data.get("user_corporate_status"),
                user_role=user_properties_data.get("user_role"),
                user_signup_date=parse_json_date(
                    user_properties_data.get("user_signup_date")
                ),
                user_status=user_properties_data.get("user_status"),
            )

            # Add the Event instance to the session
            session.add(event)

            event_metadata = EventMetadata(
                event_time=event_data.get("event_time"),
                user_id=event_data.get("user_id"),
                # Event metadata
                data_type=event_data.get("data_type"),
                event_type=event_data.get("event_type"),
                data=json.dumps(event_data.get("data")),
                # Timestamps
                client_event_time=event_data.get("client_event_time"),
                client_upload_time=event_data.get("client_upload_time"),
                processed_time=event_data.get("processed_time"),
                server_upload_time=event_data.get("server_upload_time"),
                server_received_time=event_data.get("server_received_time"),
            )

            # Add the EventMetadata instance to the session
            session.add(event_metadata)

        # Commit the session to save the instances to the database (for every event for debugging)
        try:
            session.commit()
            events_saved = True  # Reassign value if commit is successful
        except Exception as e:
            print(
                f"An error occurred ({e}) saving event: {event.event_time} for user: {event.user_id}."
            )
            session.rollback()

    session.close()
    return events_saved
