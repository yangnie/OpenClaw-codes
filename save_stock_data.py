
import sqlite3
import json
from datetime import datetime
import sys

def init_db(db_path="stock_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            last_price REAL,
            change_value REAL,
            change_percent REAL,
            record_date TEXT NOT NULL,
            record_time TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS options (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            expiration_date TEXT NOT NULL,
            strike_price REAL,
            option_type TEXT NOT NULL,
            last_price REAL,
            delta REAL,
            gamma REAL,
            theta REAL,
            vega REAL,
            rho REAL,
            phi REAL,
            bid_iv REAL,
            mid_iv REAL,
            ask_iv REAL,
            record_date TEXT NOT NULL,
            record_time TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def save_data(data, db_path="stock_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now = datetime.now()
    record_date = now.strftime("%Y-%m-%d")
    record_time = now.strftime("%H:%M:%S")

    # Stock data
    if "stocks" in data:
        for stock in data["stocks"]:
            try:
                cursor.execute("""
                    INSERT INTO stocks (symbol, last_price, change_value, change_percent, record_date, record_time)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    stock.get("symbol"),
                    stock.get("last_price"),
                    stock.get("change_value"),
                    stock.get("change_percent"),
                    record_date,
                    record_time
                ))
            except Exception as e:
                print(f"[ERROR SAVE] Failed to insert stock {stock.get("symbol")}: {e}")

    # Option data (put options only as per user's previous request)
    if "options" in data and "put" in data["options"]:
        option = data["options"]["put"]
        try:
            cursor.execute("""
                INSERT INTO options (symbol, expiration_date, strike_price, option_type, last_price, delta, gamma, theta, vega, rho, phi, bid_iv, mid_iv, ask_iv, record_date, record_time)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                option.get("symbol"),
                option.get("expiration_date"),
                option.get("strike_price"),
                "Put", # Hardcoded as "Put" as per user request to only save put options
                option.get("last_price"),
                option.get("delta"),
                option.get("gamma"),
                option.get("theta"),
                option.get("vega"),
                option.get("rho"),
                option.get("phi"),
                option.get("bid_iv"),
                option.get("mid_iv"),
                option.get("ask_iv"),
                record_date,
                record_time
            ))
        except Exception as e:
            print(f"[ERROR SAVE] Failed to insert put option for {option.get("symbol")}: {e}")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        data_str = sys.argv[1]
        try:
            data = json.loads(data_str)
            init_db()
            save_data(data)
            print("Data saved to stock_data.db successfully.")
        except json.JSONDecodeError:
            print(f"[ERROR MAIN] Invalid JSON data provided: {data_str}")
        except Exception as e:
            print(f"[ERROR MAIN] An error occurred in main execution: {e}")
    else:
        print("Usage: python save_stock_data.py '<json_data>'")
