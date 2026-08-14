from app import app

import os
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, '../data/directory.db')

import sqlite3

if __name__ == "__main__":
    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()
        print("Database Connection Initiated")

        conn.execute("DROP TABLE IF EXISTS Directories")
        conn.execute("DROP TABLE IF EXISTS Files")
        print("Tables Reset")

        query = """CREATE TABLE IF NOT EXISTS Directories (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            parent_id INTEGER,
            name TEXT NOT NULL,
            CONSTRAINT lk_parent
            FOREIGN KEY (parent_id)
            REFERENCES Directories(id)
        )"""
        cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY NOT NULL,
            directory_id INTEGER,
            name TEXT,
            CONSTRAINT fk_directory
            FOREIGN KEY (directory_id)
            REFERENCES Directories(id)
        )"""
        cursor.execute(query)
        print("Tables Created")

        cursor.execute("INSERT INTO Directories (name) VALUES ('root')")


        cursor.close()
        conn.commit()

    except sqlite3.Error as e:
        print(f"An Error Occurred - {e}")
    finally:
        if conn:
            conn.close()
            print("Database Connection Closed")

    try:
        conn = sqlite3.connect(filename)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Directories")

        result = cursor.fetchone()
        print(f"id: {result[0]}, parent_id: {result[1]}, name: {result[2]}")
        cursor.close()

    except sqlite3.Error as e:
        print(f"An Error Occurred - {e}")
    finally:
        if conn:
            conn.close()
            print("Database Connection Closed")

    app.run()
