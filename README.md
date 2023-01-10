# study-time

Desktop study session tracker built with Tkinter and SQLite.

## Why This Project Exists

Tracking focused study time manually is inconsistent. This app records each session with start time, end time, focused time, and non-focused time so you can review your study habits.

## What It Does

1. Runs a stopwatch UI for active study sessions.
2. Supports pause/play to separate focused and non-focused time.
3. Stores every session in a local SQLite database.
4. Shows historical records in overview or date-wise detailed mode.
5. Supports both CLI and simple dialog-based record viewing.

## Tech Stack

1. Python
2. Tkinter for UI
3. SQLite for persistence
4. python-dotenv for initialization state

## Project Structure

- study_time.py: main application entrypoint
- schema.sql: database schema
- stopwatch.py / study_calc.py: helper scripts
- study_sessions.db: runtime-generated local database

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python study_time.py
```

## Data Model

The app creates a table with:

- date
- start_time
- end_time
- study_time (seconds)
- other_time (seconds)

Schema file: schema.sql

## Limitations

1. UI is desktop-only (Tkinter).
2. Uses local SQLite file (no cloud sync).
3. Font availability may vary by system.

## What I Built

1. Stopwatch workflow with start/stop and pause/play state transitions.
2. Local persistence layer and session aggregation queries.
3. Dual record-display flow (GUI prompt and CLI fallback).

## Roadmap

1. Add weekly and monthly charts.
2. Add CSV export for session history.
3. Add reminders and target-based alerts.
4. Add tests for database query methods.
