import sqlite3
from config import DB_NAME

def initialize_database():
    print(f"Initializing DataBase: {DB_NAME}...")
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #Creates the Telemetry table
    cursor.execute('''
                CREATE TABLE IF NOT EXISTS telemetry (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   timestamp REAL NOT NULL,
                   flight_id TEXT NOT NULL,
                   altitude REAL NOT NULL,
                   velocity REAL NOT NULL,
                   heading REAL NOT NULL,
                   anomaly_detected INTEGER DEFAULT 0
                   )
                   ''')
    
    conn.commit()
    conn.close()
    print("Database and table successfully created!")

if __name__ == "__main__":
    initialize_database()