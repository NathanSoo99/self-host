import sqlite3
from . import db_filename

def get_directory():
    pass

def create_directory(parent_id, name):
    try:
        conn = sqlite3.connect(db_filename)
    except sqlite3.OperationalError as e:
        print(f"Unable to connect to Database - {e}")
        return None

    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    try:
        query = "INSERT INTO Directories (parent_id, name) VALUES (:parent_id, :name) RETURNING *"
        query_parameters = {"parent_id": parent_id, "name": name}
        cursor.execute(query, query_parameters)
        result = cursor.fetchone()
    except sqlite3.IntegrityError as e:
        print(f"Integrity Error - {e}")
        cursor.close()
        conn.close()
        return None

    cursor.close()
    conn.commit()
    conn.close()

    return result

        
    
    


def modify_directory():
    pass

def delete_directory():
    pass

def get_file():
    pass

def add_file():
    pass

def modify_file():
    pass

def delete_file():
    pass

"""
    row = cursor.fetchone()
    directory_id = row[0]

    file_identifier = uuid.uuid4().bytes

    query = "INSERT INTO Files (directory_id, name, uuid) VALUES (:directory_id, :name, :uuid) RETURNING *"
    query_data = {
        "directory_id": directory_id,
        "name": "file 1",
        "uuid": file_identifier
    }
    cursor.execute(query, query_data)
    result = cursor.fetchone()
    print(f"id: {result[0]}, directory_id: {result[1]}, name: {result[2]}, uuid: {str(uuid.UUID(bytes=result[3]))}")
"""