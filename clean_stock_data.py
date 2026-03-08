
import sqlite3

def clean_data(db_path="stock_data.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete incorrect stock data
    cursor.execute("DELETE FROM stocks WHERE last_price IS NULL")
    deleted_stocks = cursor.rowcount
    print(f"Deleted {deleted_stocks} incorrect stock records.")

    # Delete incorrect option data
    cursor.execute("DELETE FROM options WHERE last_price IS NULL")
    deleted_options = cursor.rowcount
    print(f"Deleted {deleted_options} incorrect option records.")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    clean_data()
