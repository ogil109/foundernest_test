import os
import sqlite3

db_path = os.getenv("DATABASE_PATH", "/results/database.db")


def get_weekly_active_users() -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS weekly_active_users (
        user_id BIGINT NOT NULL,
        week TEXT NOT NULL
    )"""
    )

    insert_query = """
    INSERT INTO weekly_active_users(week, user_id)
    SELECT
        strftime('%Y-W%W', date) AS week,
        user_id
    FROM events
    GROUP BY week, user_id
    ORDER BY week;
    """

    cursor.execute(insert_query)
    conn.commit()

    # Fetch and write txt file counting weekly active users
    select_query = "SELECT week, COUNT(user_id) FROM weekly_active_users GROUP BY week ORDER BY week;"
    cursor.execute(select_query)
    results = cursor.fetchall()

    os.makedirs("/results", exist_ok=True)
    with open("/results/weekly_active_users.txt", "w", encoding="utf-8") as file:
        for row in results:
            file.write(f"{row[0]}: {row[1]}\n")

    conn.close()


def get_weekly_active_corporate_users() -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS weekly_active_corporate_users (
        user_corporate_id BIGINT,
        week TEXT NOT NULL
    )"""
    )

    insert_query = """
    INSERT INTO weekly_active_corporate_users(week, user_corporate_id)
    SELECT
        strftime('%Y-W%W', e.date) AS week,
        up.user_corporate_id
    FROM events e
    INNER JOIN user_properties up ON e.user_id = up.user_id
    GROUP BY week, up.user_corporate_id
    ORDER BY week;
    """

    cursor.execute(insert_query)
    conn.commit()

    # Fetch and write txt file counting weekly active corporate users
    select_query = "SELECT week, COUNT(user_corporate_id) FROM weekly_active_corporate_users GROUP BY week ORDER BY week;"
    cursor.execute(select_query)
    results = cursor.fetchall()

    os.makedirs("/results", exist_ok=True)
    with open(
        "/results/weekly_active_corporate_users.txt", "w", encoding="utf-8"
    ) as file:
        for row in results:
            file.write(f"{row[0]}: {row[1]}\n")

    conn.close()


def events_stats_users() -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS events_stats_users (
        week TEXT NOT NULL,
        avg_events_per_user REAL,
        max_events_per_user INTEGER,
        min_events_per_user INTEGER
    )"""
    )

    insert_query = """
    WITH Week_Events AS (
        SELECT
            user_id,
            strftime('%Y-W%W', date) AS week,
            COUNT(*) AS events_count
        FROM events
        GROUP BY user_id, week
    ),
    Week_Stats AS (
        SELECT
            week,
            AVG(events_count) AS avg_events_per_user,
            MAX(events_count) AS max_events_per_user,
            MIN(events_count) AS min_events_per_user
        FROM Week_Events
        GROUP BY week
    )
    INSERT INTO events_stats_users (week, avg_events_per_user, max_events_per_user, min_events_per_user)
    SELECT week, avg_events_per_user, max_events_per_user, min_events_per_user
    FROM Week_Stats
    ORDER BY week;
    """

    cursor.execute(insert_query)
    conn.commit()

    # Fetch and write txt file
    select_query = "SELECT week, avg_events_per_user, max_events_per_user, min_events_per_user FROM events_stats_users ORDER BY week;"
    cursor.execute(select_query)
    results = cursor.fetchall()

    os.makedirs("/results", exist_ok=True)
    with open("/results/events_stats_users.txt", "w", encoding="utf-8") as file:
        for row in results:
            file.write(
                f"{row[0]} = Avg Events Per User: {row[1]:.2f}, Max Events Per User: {row[2]}, Min Events Per User: {row[3]}\n"
            )

    conn.close()


def events_stats_corporate_users() -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS events_stats_corporate_users (
        week TEXT NOT NULL,
        avg_events_per_corporate_user REAL,
        max_events_per_corporate_user INTEGER,
        min_events_per_corporate_user INTEGER
    )"""
    )

    insert_query = """
    WITH Corporate_Week_Events AS (
        SELECT
            up.user_corporate_id,
            strftime('%Y-W%W', date) AS week,
            COUNT(*) AS events_count
        FROM events e
        INNER JOIN user_properties up ON e.user_id = up.user_id
        GROUP BY up.user_corporate_id, week
    ),
    Corporate_Week_Stats AS (
        SELECT
            week,
            AVG(events_count) AS avg_events_per_corporate_user,
            MAX(events_count) AS max_events_per_corporate_user,
            MIN(events_count) AS min_events_per_corporate_user
        FROM Corporate_Week_Events
        GROUP BY week
    )
    INSERT INTO events_stats_corporate_users (week, avg_events_per_corporate_user, max_events_per_corporate_user, min_events_per_corporate_user)
    SELECT week, avg_events_per_corporate_user, max_events_per_corporate_user, min_events_per_corporate_user
    FROM Corporate_Week_Stats
    ORDER BY week;
    """

    cursor.execute(insert_query)
    conn.commit()

    # Fetch and write txt file
    select_query = "SELECT week, avg_events_per_corporate_user, max_events_per_corporate_user, min_events_per_corporate_user FROM events_stats_corporate_users ORDER BY week;"
    cursor.execute(select_query)
    results = cursor.fetchall()

    os.makedirs("/results", exist_ok=True)
    with open(
        "/results/events_stats_corporate_users.txt", "w", encoding="utf-8"
    ) as file:
        for row in results:
            file.write(
                f"{row[0]} = Avg Events Per Corporate User: {row[1]:.2f}, Max Events Per Corporate User: {row[2]}, Min Events Per Corporate User: {row[3]}\n"
            )

    conn.close()
