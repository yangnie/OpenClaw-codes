# OpenClaw Stock Monitor

This repository contains Python scripts and a SQL schema for monitoring stock and option data within an OpenClaw agent environment. The scripts allow for fetching, saving, cleaning, and reading historical stock and put option data into a SQLite database.

## Files

-   `save_stock_data.py`: A Python script responsible for initializing the SQLite database tables (if they don't exist) and inserting stock and put option data. It expects data in a specific JSON format as a command-line argument.
-   `read_stock_data.py`: A Python script to query and display historical stock and put option data from the SQLite database. It supports filtering by date range.
-   `clean_stock_data.py`: A Python script to remove any incomplete or erroneous data entries (where `last_price` is NULL) from the database.
-   `schema.sql`: Defines the table structures for `stocks` and `options` in a SQLite database.

## Database Setup

To initialize the SQLite database (`stock_data.db`) and create the necessary tables, you can run the `save_stock_data.py` script once with dummy data, or use the `schema.sql` file:

```bash
sqlite3 stock_data.db < schema.sql
```

This will create `stock_data.db` in your current directory.

## Usage

### `save_stock_data.py`

This script is primarily intended to be called by an automated process (e.g., an OpenClaw cron job) that fetches real-time data. It expects a JSON string as a command-line argument.

Example (for testing):

```bash
python3 save_stock_data.py '{
  "stocks": [
    {
      "symbol": "TSLA",
      "last_price": 395.00,
      "change_value": 0.00,
      "change_percent": 0.00
    },
    {
      "symbol": "CRWV",
      "last_price": 79.91,
      "change_value": 8.95,
      "change_percent": 11.2
    }
  ],
  "options": {
    "put": {
      "symbol": "TSLA",
      "expiration_date": "2026-03-27",
      "strike_price": 380.00,
      "last_price": 10.50,
      "delta": -0.3000,
      "gamma": 0.00750,
      "theta": -0.3500,
      "vega": 0.3800,
      "rho": 0.1500,
      "phi": -0.1600,
      "bid_iv": 0.4500,
      "mid_iv": 0.4600,
      "ask_iv": 0.4700
    }
  }
}'
```

### `read_stock_data.py`

View historical stock and option data. By default, it displays all valid entries. You can filter by date range using the `--range` argument.

```bash
# Display all valid data
python3 read_stock_data.py

# Display data from the last 1 day (e.g., yesterday and today if today is empty)
python3 read_stock_data.py --range "1 day"

# Display data from the last N days
python3 read_stock_data.py --range "N days"

# Display data from the last week
python3 read_stock_data.py --range "1 week"

# Display data from the last month
python3 read_stock_data.py --range "1 month"
```

### `clean_stock_data.py`

Removes any incomplete data entries from the `stocks` and `options` tables (records where `last_price` is NULL).

```bash
python3 clean_stock_data.py
```

## OpenClaw Cron Job Integration

For automated daily monitoring and saving, these scripts are integrated into an OpenClaw cron job. The cron job is configured to:

1.  Fetch the latest TSLA and CRWV stock data and TSLA put option data.
2.  Format this data into a JSON string that `save_stock_data.py` expects.
3.  Execute `python3 save_stock_data.py` with the JSON data.
4.  Summarize and present the results to the user.

(Note: The full cron job payload is managed within the OpenClaw agent's configuration.)
