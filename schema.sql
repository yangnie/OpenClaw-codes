
CREATE TABLE IF NOT EXISTS stocks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL,
    last_price REAL,
    change_value REAL,
    change_percent REAL,
    record_date TEXT NOT NULL,
    record_time TEXT NOT NULL
);

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
);
