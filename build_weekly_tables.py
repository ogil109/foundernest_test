"""
This script builds the weekly tables for the called week.

Args:
    week_to_process (str): The week in the format %Y-W%W to process and insert data for.

Returns:
    None
"""

import os
import sqlite3
import sys
from datetime import datetime

from app.database.transformation import (
    events_stats_corporate_users,
    events_stats_users,
    get_weekly_active_corporate_users,
    get_weekly_active_users,
)

# Database connection and cursor init
db_path = os.getenv("DATABASE_PATH", "/results/database.db")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS processed_weeks (week TEXT)""")


def is_week_already_processed(week_to_check) -> bool:
    cursor.execute("SELECT week FROM processed_weeks WHERE week = ?", (week_to_check,))
    result = cursor.fetchone()
    if result:
        print(f"\nWeek {week_to_check} has already been processed.\n")
        return True
    else:
        return False


def mark_week_as_processed(week_to_mark):
    cursor.execute("INSERT INTO processed_weeks (week) VALUES (?)", (week_to_mark,))
    conn.commit()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a week argument in the format %Y-W%W")
        sys.exit(1)

    week_to_process = sys.argv[1]

    try:
        datetime.strptime(week_to_process, "%Y-W%W")
    except ValueError:
        print(
            "Invalid week format. Please provide a week argument in the format %Y-W%W"
        )
        sys.exit(1)

    # Reopen connection if closed from previous run
    conn = sqlite3.connect(db_path)

    # Check if week has already been processed, if not, process it
    if not is_week_already_processed(week_to_process):
        events_stats_users(week_to_process)
        events_stats_corporate_users(week_to_process)
        get_weekly_active_users(week_to_process)
        get_weekly_active_corporate_users(week_to_process)
        # Mark week as processed
        mark_week_as_processed(week_to_process)

    conn.close()
