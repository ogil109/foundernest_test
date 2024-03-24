from datetime import datetime

from app import load_data
from app.database.transformation import (
    events_stats_corporate_users,
    events_stats_users,
    get_weekly_active_corporate_users,
    get_weekly_active_users,
)

# Load data
start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 1, 31)
load_data(start_date, end_date)

# Insertions and stats
get_weekly_active_users()
get_weekly_active_corporate_users()
events_stats_users()
events_stats_corporate_users()
