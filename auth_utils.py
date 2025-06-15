"""Authentication utilities for retrieving user profiles."""

import psycopg2


def get_user_profile(user_id):
    """Return the subscription plan and API key for ``user_id``."""

    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="supabase",
        user="postgres",
        password="postgres",
    )
    cursor = conn.cursor()
    cursor.execute("SELECT plan, api_key FROM user_profiles WHERE id=%s", (user_id,))
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row
