from app import app, db_filename
from app.virtual_file_system import get_directory, create_directory
from app.virtual_file_system import add_file

import sqlite3

if __name__ == "__main__":

    # virtual file system setup
    # TODO remove file system hard reset
    try:
        conn = sqlite3.connect(db_filename)
    except sqlite3.OperationalError as e:
        print(f"Unable to connect to Database - {e}")
        exit()
    print("Database Connection Initiated")

    try:
        conn.execute("DROP TABLE IF EXISTS Directories")
        conn.execute("DROP TABLE IF EXISTS Files")
        cursor = conn.cursor()
        print("Tables Reset")

        query = """CREATE TABLE IF NOT EXISTS Directories (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            parent_id INTEGER,
            name TEXT NOT NULL CHECK(length(name) <= 100),
            FOREIGN KEY (parent_id) REFERENCES Directories(id)
            UNIQUE (parent_id, name)
        )"""
        cursor.execute(query)
        query = """CREATE TABLE IF NOT EXISTS Files (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            directory_id INTEGER NOT NULL,
            name TEXT NOT NULL CHECK(length(name) <= 100),
            uuid BLOB NOT NULL UNIQUE,
            FOREIGN KEY (directory_id) REFERENCES Directories(id)
            UNIQUE (directory_id, name)
        )"""
        cursor.execute(query)
        print("Tables Created")
        cursor.execute("INSERT INTO Directories (name) VALUES ('~') RETURNING *")
        result = cursor.fetchone()
        print(f"Virtual Root Directory Created - id: {result[0]}")

        cursor.close()
        conn.commit()
        conn.close()
        print("Database Connection Closed")
    except sqlite3.Error as e:
        print(f"An Error Occurred - {e}")
        exit()

    add_file("~", "hi.txt", b"\xfd\xfa\xed\x14")

    while True:
        cwd = "~"
        cmd = input(f"{cwd}$ ")

        args = cmd.split(" ")

        if args[0] == "ls":
            print(get_directory(cwd))
        elif args[0] == "mkdir":
            create_directory(cwd, args[1])
        else:
            print("invalid command")
