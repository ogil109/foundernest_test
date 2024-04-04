def cursor_count(cursor_passed, date_passed):
    """
    Executes a SQL query to count the number of events within a specific date.

    Args:
        cursor_passed (sqlite3.Cursor): The cursor object used to execute the query.
        date_passed (datetime.date): The date to count the events for.

    Returns:
        int: The number of events with the specified date. Returns 0 if no events are found.
    """
    cursor_passed.execute(
        "SELECT COUNT(*) FROM events WHERE date = ?",
        (date_passed.strftime("%Y-%m-%d"),),
    )

    result = cursor_passed.fetchone()
    # Handle days with no events
    if result is not None:
        return result[0]

    # In case of no events, return 0 instead of None
    return 0


if __name__ == "__main__":
    import os
    import sqlite3
    import sys
    from datetime import date

    from app import load_data

    try:
        date = date.fromisoformat((sys.argv[1]))
    except ValueError:
        print("\nInvalid format. Provide date in ISO format (YYYY-MM-DD)\n")
        sys.exit(1)

    # Get events for date before loading/updating
    db_path = os.getenv("DATABASE_PATH", "/results/database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    before = cursor_count(cursor, date)

    # Loading data for date (parse_date_events() will handle duplicates in case of multiple calls for the same date)
    load_data(date, date)

    # Get events for date after loading
    after = cursor_count(cursor, date)

    print(f"\nData loaded for {date}.\n")
    print(
        f"Events prior to load: {before}\nEvents after load: {after}\nNew events: {after - before}\n"
    )
