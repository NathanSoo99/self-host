import sqlite3
import os

dirname = os.path.dirname(__file__)
db_filename = os.path.join(dirname, '../../data/directory.db')

def db_connect(db_filename):
    try:
        conn = sqlite3.connect(db_filename)
    except sqlite3.OperationalError as e:
        print(f"Unable to connect to Database - {e}")
        return None
    return conn