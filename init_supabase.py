"""Initialize Supabase tables from the local schema."""

import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("SUPABASE_HOST", "localhost"),
    port=os.getenv("SUPABASE_PORT", "5432"),
    dbname=os.getenv("SUPABASE_DB", "supabase"),
    user=os.getenv("SUPABASE_USER", "postgres"),
    password=os.getenv("SUPABASE_PASSWORD", "postgres")
)

cursor = conn.cursor()

with open("schema.sql", "r", encoding="utf-8") as f:
    schema = f.read()
    cursor.execute(schema)

conn.commit()
cursor.close()
conn.close()

print("✅ Supabase Tables Initialized")
