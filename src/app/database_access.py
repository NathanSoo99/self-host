import sqlite3

def db_connect(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
    except sqlite3.OperationalError as e:
        print(f"Unable to connect to Database - {e}")
        return None
    return conn