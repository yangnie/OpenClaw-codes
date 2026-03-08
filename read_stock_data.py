
import sqlite3
import sys
from datetime import datetime, timedelta

def get_date_range_filter_sqlite(range_str):
    range_str = range_str.lower()

    if "day" in range_str:
        num_days = int(range_str.split(" ")[0]) if range_str.split(" ")[0].isdigit() else 1
        return f"-{num_days} days"
    elif "week" in range_str:
        return "-7 days"
    elif "month" in range_str:
        return "-30 days" # Approximate a month as 30 days
    else:
        return None

def read_data(db_path="stock_data.db", sqlite_date_modifier=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    base_stock_query = "SELECT symbol, last_price, change_value, change_percent, record_date, record_time FROM stocks WHERE last_price IS NOT NULL"
    base_option_query = "SELECT symbol, expiration_date, strike_price, option_type, last_price, delta, gamma, theta, vega, rho, phi, bid_iv, mid_iv, ask_iv, record_date, record_time FROM options WHERE last_price IS NOT NULL AND option_type = 'Put'"

    stock_query_params = []
    option_query_params = []

    if sqlite_date_modifier:
        stock_query = f"{base_stock_query} AND record_date >= date('now', ?) ORDER BY record_date ASC, record_time ASC"
        stock_query_params.append(sqlite_date_modifier)
        
        option_query = f"{base_option_query} AND record_date >= date('now', ?) ORDER BY record_date ASC, record_time ASC"
        option_query_params.append(sqlite_date_modifier)

    else: # No filter, get all data
        stock_query = f"{base_stock_query} ORDER BY record_date ASC, record_time ASC"
        option_query = f"{base_option_query} ORDER BY record_date ASC, record_time ASC"

    print("\n--- Stock Data ---")
    cursor.execute(stock_query, stock_query_params)
    stocks = cursor.fetchall()
    if stocks:
        for stock in stocks:
            print(f"Symbol: {stock[0]}, Last Price: {stock[1]}, Change Value: {stock[2]}, Change Percent: {stock[3]}%, Date: {stock[4]}, Time: {stock[5]}")
    else:
        print("No stock data found for the specified range.")

    print("\n--- Put Option Data ---")
    cursor.execute(option_query, option_query_params)
    options = cursor.fetchall()
    if options:
        for option in options:
            print(f"Symbol: {option[0]}, Expiration: {option[1]}, Strike: {option[2]}, Type: {option[3]}, Last Price: {option[4]}, Delta: {option[5]}, Gamma: {option[6]}, Theta: {option[7]}, Vega: {option[8]}, Rho: {option[9]}, Phi: {option[10]}, Bid IV: {option[11]}, Mid IV: {option[12]}, Ask IV: {option[13]}, Date: {option[14]}, Time: {option[15]}")
    else:
        print("No put option data found for the specified range.")

    conn.close()

if __name__ == "__main__":
    range_arg = None
    if len(sys.argv) > 2 and sys.argv[1] == "--range":
        range_arg = sys.argv[2]
    
    sqlite_date_modifier = None
    if range_arg:
        sqlite_date_modifier = get_date_range_filter_sqlite(range_arg)

    read_data(sqlite_date_modifier=sqlite_date_modifier)
