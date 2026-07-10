from app import app

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/directory.db')

import sqlite3

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(filename)
        print("Hello Database")
    except sqlite3.Error:
        print("An Error Occurred")
    finally:
        conn.close()
    app.run()
