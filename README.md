# Auto Pipeline

This repository contains automation scripts for content generation and tracking.

## Supabase Setup

1. Update `.env` with your database credentials based on `.env.sample`.
2. Start containers using `docker-compose up -d`.
3. Run `python init_supabase.py` to create the required tables from `schema.sql`.

The schema includes tables for content tracking, performance metrics, and scheduling.
