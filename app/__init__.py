from datetime import date, timedelta

from app.ingestion.extract import get_date_events


def load_data(start_date: date, end_date: date) -> None:
    """
    Load user events data for a given date range.

    Args:
        start_date (date): The start date of the date range, format: YYYY-MM-DD.
        end_date (date): The end date of the date range, format: YYYY-MM-DD.
    """
    no_event_days = []
    for dt in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=dt)
        events_saved = get_date_events(date.strftime("%Y-%m-%d"))

        if not events_saved:
            no_event_days.append(date.strftime("%Y-%m-%d"))

    if no_event_days:
        print(f"\nNo events found for {no_event_days}.\n")
