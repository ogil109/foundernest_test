from datetime import datetime, timedelta

from app.ingestion.load import get_date_events


def load_data() -> None:
    # Load data from January
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 1, 31)

    for dt in range((end_date - start_date).days + 1):
        date = start_date + timedelta(days=dt)
        get_date_events(date.strftime("%Y-%m-%d"))
