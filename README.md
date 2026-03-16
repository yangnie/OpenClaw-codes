# OpenClaw-codes: Tradier Market Data Monitor

This repository contains a Python script, `fetch_tradier_data.py`, designed to interact with the Tradier API for fetching stock and option market data, and then persisting this data into a local SQLite database. It's built for use within an OpenClaw agent environment to enable automated market data monitoring and analysis.

The script also manages a `monitor_target` table, allowing you to easily add, remove, activate, or deactivate stock and option symbols for automated fetching.

## Features

-   **Stock Data Fetching:** Retrieves real-time stock quotes for specified symbols.
-   **Option Data Fetching:** Retrieves detailed option chain data for specified option symbols, including Greeks (delta, gamma, theta, vega, rho), open interest, and volume.
-   **SQLite Integration:** Stores fetched stock and option data into a `tradier_market_data.db` SQLite database, adhering to a defined schema.
-   **Monitor Target Management:** A `monitor_target` table in the database allows for dynamic management of symbols to be monitored, replacing the need for direct JSON input for fetching.
-   **Command-Line Interface:** Easy-to-use commands for database initialization, target management, data fetching, and historical data querying.
-   **Debug Logging:** Provides detailed debug output for troubleshooting, especially for option symbol parsing and fetching.

## Setup

1.  **Navigate to the `OpenClaw-codes` directory:**
    ```bash
    cd ~/.openclaw/workspace/OpenClaw-codes
    ```

2.  **Create and activate a Python virtual environment (if you haven't already):**
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install required Python packages:**
    ```bash
    pip install requests Flask
    ```

4.  **Set your Tradier API Key as an environment variable:**
    Obtain your API key from [Tradier](https://developer.tradier.com/).
    ```bash
    export TRADIER_API_KEY="YOUR_TRADIER_API_KEY_HERE"
    # Example: export TRADIER_API_KEY="Fn6Yb76XhAtPCUXeLLRJGxuPsBVy"
    ```
    Replace `YOUR_TRADIER_API_KEY_HERE` with your actual key.

## `fetch_tradier_data.py` Usage

The script `fetch_tradier_data.py` supports several commands: `init-db`, `add-target`, `remove-target`, `list-targets`, `activate-target`, `deactivate-target`, `fetch`, and `query`.

### Initialize Database

This command initializes the `tradier_market_data.db` SQLite database and creates the `stocks`, `options`, and `monitor_target` tables based on the defined schema. You only need to run this once.

```bash
python fetch_tradier_data.py init-db
```

### Manage Monitoring Targets

These commands allow you to add, remove, list, activate, and deactivate stock and option symbols in the `monitor_target` table.

#### Add Target
Adds a new symbol to the `monitor_target` table. Specify the `symbol` and `type` (`stock` or `option`).

```bash
python fetch_tradier_data.py add-target TSLA stock
python fetch_tradier_data.py add-target CRWV stock
python fetch_tradier_data.py add-target TSLA260327P00380000 option
python fetch_tradier_data.py add-target TSLA260417P00365000 option
```

#### List Targets
Lists all monitoring targets, or filters by active/inactive status.

```bash
# List all targets
python fetch_tradier_data.py list-targets

# List only active targets
python fetch_tradier_data.py list-targets active

# List only inactive targets
python fetch_tradier_data.py list-targets inactive
```

#### Activate/Deactivate Target
Changes the `is_active` status of a symbol.

```bash
# Activate a target
python fetch_tradier_data.py activate-target TSLA

# Deactivate a target
python fetch_tradier_data.py deactivate-target CRWV
```

#### Remove Target
Removes a symbol from the `monitor_target` table.

```bash
python fetch_tradier_data.py remove-target CRWV
```

### Fetch Market Data

This command fetches market data for all **active** symbols defined in the `monitor_target` table. The fetched data (stocks and options) is then saved into the `stocks` and `options` tables in `tradier_market_data.db`.

```bash
python fetch_tradier_data.py fetch
```

#### Fetch with Debugging
To enable detailed debug logging for a specific option symbol during a `fetch` operation, use the `--debug-option` flag. This will print verbose debug messages related to parsing and fetching that particular option.

```bash
python fetch_tradier_data.py fetch --debug-option TSLA260327P00380000
```

### Query Saved Data

Queries historical stock or option data from the `tradier_market_data.db` database.

```bash
# Query the 10 most recent stock entries
python fetch_tradier_data.py query stocks

# Query the 5 most recent stock entries for TSLA
python fetch_tradier_data.py query stocks TSLA 5

# Query the 10 most recent option entries
python fetch_tradier_data.py query options

# Query the 3 most recent option entries for a specific option symbol
python fetch_tradier_data.py query options TSLA260327P00380000 3
```

## `api_server.py` (Flask Web API)

This Flask application provides a web API interface to all the functionalities of the `fetch_tradier_data.py` script, including data fetching, database querying, and monitoring target management. It uses token-based authentication.

### Setup

1.  **Ensure `fetch_tradier_data.py` prerequisites are met** (Python, virtual environment, `requests` installed).
2.  **Install Flask** in your virtual environment (if not already installed during `fetch_tradier_data.py` setup):
    ```bash
    pip install Flask
    ```
3.  **Generate and Set API Authentication Token:**
    Choose a strong, secret token. You can generate one using Python:
    ```bash
    python3 -c 'import secrets; print(secrets.token_hex(32))'
    ```
    Then, set it as an environment variable before running the API server:
    ```bash
    export API_AUTH_TOKEN="your_generated_secret_api_token_here"
    ```
    Replace `"your_generated_secret_api_token_here"` with your actual token.

### Running the API Server

Navigate to the `OpenClaw-codes` directory and run the `api_server.py` script within your activated virtual environment. Ensure `API_AUTH_TOKEN` and `TRADIER_API_KEY` are set in the environment where the server runs.

```bash
# From within the OpenClaw-codes directory:
source ../venv/bin/activate  # Or whatever your venv path is relative to workspace root
export API_AUTH_TOKEN="your_generated_secret_api_token_here"
export TRADIER_API_KEY="YOUR_TRADIER_API_KEY_HERE" # Required for fetch_tradier_data.py
python3 api_server.py
```
The server will run on `http://0.0.0.0:5000`.

### API Endpoints

All endpoints (except `/`) require token-based authentication. Include an `Authorization` header with a `Bearer` token (your `API_AUTH_TOKEN`).

**Authentication Header Example:** `-H "Authorization: Bearer ${API_AUTH_TOKEN}"`

#### 1. Welcome Message (GET `/`)
*   **Description:** Basic endpoint to confirm the server is running.
*   **Authentication:** None
```bash
curl http://localhost:5000/
```
**Expected Output:** `{"message": "Tradier Market Data API. Use /api/fetch, /api/query, /api/targets, etc."}`

#### 2. Initialize Database (POST `/api/init-db`)
*   **Description:** Initializes (or re-initializes) the SQLite database.
*   **Authentication:** Required
```bash
curl -X POST \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  http://localhost:5000/api/init-db
```
**Expected Output:** `{"message": "Database initialized successfully."}`

#### 3. Add Monitoring Target (POST `/api/target`)
*   **Description:** Adds a new stock or option symbol to be monitored.
*   **Authentication:** Required
*   **Request Body:** `{"symbol": "STRING", "type": "stock" | "option"}`
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  -d '{"symbol": "MSFT", "type": "stock"}' \
  http://localhost:5000/api/target
```
**Expected Output:** `{"message": "Target MSFT (stock) added successfully."}`

#### 4. List Monitoring Targets (GET `/api/targets`)
*   **Description:** Retrieves a list of all configured monitoring targets.
*   **Authentication:** Required
*   **Optional Query Parameter:** `status` (`active` | `inactive` | `all`)
    *   Example: `GET /api/targets?status=active`
```bash
# List all targets
curl -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  http://localhost:5000/api/targets

# List only active targets
curl -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  "http://localhost:5000/api/targets?status=active"
```
**Expected Output:** `{"targets": [{"symbol": "AAPL", "type": "stock", "active": true}, ...]}`

#### 5. Deactivate/Activate Target (POST `/api/target/<symbol>/<action>`)
*   **Description:** Changes the active status of a specific monitoring target.
*   **Authentication:** Required
*   **Path Parameters:** `symbol` (e.g., `AAPL`), `action` (`activate` | `deactivate`)
```bash
# Deactivate a target
curl -X POST \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  http://localhost:5000/api/target/MSFT/deactivate

# Activate a target
curl -X POST \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  http://localhost:5000/api/target/MSFT/activate
```
**Expected Output:** `{"message": "Target MSFT deactivated."}`

#### 6. Remove Monitoring Target (DELETE `/api/target`)
*   **Description:** Removes a symbol from the monitoring targets.
*   **Authentication:** Required
*   **Request Body:** `{"symbol": "STRING"}`
```bash
curl -X DELETE \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  -d '{"symbol": "MSFT"}' \
  http://localhost:5000/api/target
```
**Expected Output:** `{"message": "Target MSFT removed successfully."}`

#### 7. Fetch Market Data (POST `/api/fetch`)
*   **Description:** Triggers `fetch_tradier_data.py` to fetch data for all active targets.
*   **Authentication:** Required
```bash
curl -X POST \
  -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  http://localhost:5000/api/fetch
```
**Expected Output:** `{"timestamp": "...", "data": [...]}` (contains fetched stock/option data)

#### 8. Query Saved Data (GET `/api/query/<table_name>`)
*   **Description:** Queries historical data from the database.
*   **Authentication:** Required
*   **Path Parameters:** `table_name` (`stocks` | `options`)
*   **Optional Query Parameters:** `symbol` (e.g., `TSLA`), `limit` (default `10`)
    *   Example: `GET /api/query/stocks?symbol=TSLA&limit=5`
```bash
# Query recent stock data for TSLA
curl -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  "http://localhost:5000/api/query/stocks?symbol=TSLA&limit=5"

# Query recent option data
curl -H "Authorization: Bearer ${API_AUTH_TOKEN}" \
  "http://localhost:5000/api/query/options?limit=3"
```
**Expected Output:** A JSON array of stock or option data.

## Database Schema (`tradier_market_data.db`)

The database structure aligns with `schema.sql` in this repository.

### `stocks` Table
Stores historical stock data.

| Column          | Type    | Description                               |
| :-------------- | :------ | :---------------------------------------- |
| `id`            | INTEGER | Primary Key, Auto-increment               |
| `symbol`        | TEXT    | Stock ticker symbol (e.g., TSLA)          |
| `last_price`    | REAL    | Last traded price                         |
| `change_value`  | REAL    | Change in price                           |
| `change_percent`| REAL    | Percentage change in price                |\n| `volume`        | INTEGER | Trading volume                            |\n| `fetch_timestamp`| DATETIME| Timestamp when data was fetched           |\n\n### `options` Table\nStores historical option contract data.\n\n| Column          | Type    | Description                               |\n| :-------------- | :------ | :---------------------------------------- |\n| `id`            | INTEGER | Primary Key, Auto-increment               |\n| `symbol`        | TEXT    | OCC Option Symbol (e.g., TSLA260327P00380000) |\n| `underlying`    | TEXT    | Underlying stock symbol                   |\n| `expiration_date`| TEXT   | Expiration date (YYYY-MM-DD)              |\n| `strike_price`  | REAL    | Strike price                              |\n| `option_type`   | TEXT    | Type of option (\'call\' or \'put\')          |\n| `last_price`    | REAL    | Last traded price                         |\n| `delta`         | REAL    | Option Delta                              |\n| `gamma`         | REAL    | Option Gamma                              |\n| `theta`         | REAL    | Option Theta                              |\n| `vega`          | REAL    | Option Vega                               |\n| `rho`           | REAL    | Option Rho                                |\n| `bid_iv`        | REAL    | Bid Implied Volatility                    |\n| `mid_iv`        | REAL    | Mid Implied Volatility                    |\n| `ask_iv`        | REAL    | Ask Implied Volatility                    |\n| `open_interest` | INTEGER | Open Interest                             |\n| `volume`        | INTEGER | Trading volume                            |\n| `fetch_timestamp`| DATETIME| Timestamp when data was fetched           |\n\n### `monitor_target` Table\nStores the list of symbols to be actively monitored.\n\n| Column          | Type    | Description                               |\n| :-------------- | :------ | :---------------------------------------- |\n| `id`            | INTEGER | Primary Key, Auto-increment               |\n| `symbol`        | TEXT    | Stock or option symbol (UNIQUE)           |\n| `type`          | TEXT    | \'stock\' or \'option\'                       |\n| `is_active`     | INTEGER | 1 for active, 0 for inactive (DEFAULT 1)  |\n