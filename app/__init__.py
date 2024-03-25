from datetime import date, timedelta

from app.ingestion.extract import get_date_events


def load_data(start_date: date, end_date: date) -> None:
    """
    Load user events data for a given date range.

    Args:
        start_date (date): The start date of the date range, format: YYYY-MM-DD.
        end_date (date): The end date of the date range, format: YYYY-MM-DD.
    """
    for dt in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=dt)
        get_date_events(date.strftime("%Y-%m-%d"))
