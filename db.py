import sqlite3

DATABASE_NAME = "database.db"

def get_db_connection():
    """Establish and return a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Enables column access by name
    return conn

def create_tables():
    """Create necessary tables if they do not exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            temperature REAL,
            humidity REAL,
            rainfall REAL,
            area REAL,
            weather TEXT,
            corn_type TEXT,
            predicted_yield REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def insert_prediction(temperature, humidity, rainfall, area, weather, corn_type, predicted_yield):
    """Insert a new prediction into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO predictions (temperature, humidity, rainfall, area, weather, corn_type, predicted_yield)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (temperature, humidity, rainfall, area, weather, corn_type, predicted_yield))

    conn.commit()
    conn.close()

def fetch_predictions():
    """Retrieve all stored predictions."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]  # Convert rows to dictionary format for easy JSON conversion

# Create tables when the module is imported
create_tables()
