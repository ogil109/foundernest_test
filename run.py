from datetime import datetime

from app import load_data
from app.database.transformation import (
    events_stats_corporate_users,
    events_stats_users,
    get_weekly_active_corporate_users,
    get_weekly_active_users,
)

# Date range to load data from
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)

# Load data and save to db
load_data(start_date, end_date)

# Insertions and stats
get_weekly_active_users()
get_weekly_active_corporate_users()
events_stats_users()
events_stats_corporate_users()

# Print how to load specific date
print(
    f"\nData loaded (results in TXT in results folder). To load data for a specific date outside of January, run:\npython load_date.py YYYY-MM-DD\n"
)
