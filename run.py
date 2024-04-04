from datetime import datetime, timedelta

from app import load_data
from app.database.transformation import (
    events_stats_corporate_users,
    events_stats_users,
    get_weekly_active_corporate_users,
    get_weekly_active_users,
)
from build_weekly_tables import mark_week_as_processed

# Date range to load data from
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)

# Load data and save to db
load_data(start_date, end_date)

# Calculate the weeks between the start and end dates in the format %Y-W%W and loop through the functions to use them for every week
weeks = [
    (start_date + timedelta(weeks=i)).strftime("%Y-W%W")
    for i in range((end_date - start_date).days // 7)
]
for week in weeks:
    get_weekly_active_users(week)
    get_weekly_active_corporate_users(week)
    events_stats_users(week)
    events_stats_corporate_users(week)
    # Mark week as processed
    mark_week_as_processed(week)

# Print how to load specific date
print(
    f"\nData loaded (results in TXT in results folder).\nTo load data for a specific date outside of January, run: python load_date.py %YYYY-%MM-%DD (i.e. 2024-01-01)\nTo build the analytics tables for a week, run: python build_weekly_tables.py YYYY-W%W (i.e. 2024-W02\n"
)
