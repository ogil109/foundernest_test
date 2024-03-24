if __name__ == "__main__":
    import sqlite3
    import sys
    from datetime import datetime

    from app import load_data

    try:
        date = datetime.fromisoformat(sys.argv[1])
    except ValueError:
        print("Invalid format. Provide date in ISO format (YYYY-MM-DD).")
        sys.exit(1)

    load_data(date, date)
    print(f"Data loaded for {date}. Rows inserted:")

    # Print saved events count
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM events WHERE date = ?",
        (date.strftime("%Y-%m-%d"),),
    )
    print(f"Events inserted: {cursor.fetchone()[0]}")
