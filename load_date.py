if __name__ == "__main__":
    import os
    import sqlite3
    import sys
    from datetime import datetime

    from app import load_data

    try:
        dt = datetime.fromisoformat((sys.argv[1]))
        date = dt.date()
    except ValueError:
        print("Invalid format. Provide date in ISO format (YYYY-MM-DD).")
        sys.exit(1)

    load_data(date, date)
    print(f"\nData loaded for {date}.")

    # Print saved events count
    db_path = os.getenv("DATABASE_PATH", "/results/database.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT COUNT(*) FROM events WHERE date = ?",
        (date.strftime("%Y-%m-%d"),),
    )
    print(f"\nEvents captured: {cursor.fetchone()[0]}\n")
