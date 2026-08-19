import sqlite3
from . import db_filename
from database_access import db_connect

def get_directory_id(virtual_path, cursor):
    directory_chain = virtual_path.split("/")[1::]
    parent_directory = None

    # traverse path to find directory id
    for directory in directory_chain:
        query = """
            SELECT id, parent_id, name
            FROM Directories
            WHERE name = :directory AND parent_id = :parent_id
        """
        query_parameters = {
            "directory": directory,
            "parent_id": parent_directory
        }
        cursor.execute(query, query_parameters)
        query_result = cursor.fetchone()
        if query_result is None:
            parent_directory = None
            break
        else:
            parent_directory = query_result[0]

    return parent_directory
    

def get_directory(virtual_path):
    conn = db_connect(db_filename)
    if conn is None:
        return None

    cursor = conn.cursor()

    directory_id = get_directory_id(virtual_path, cursor)

    if directory_id is not None:
        results = {
            "directories": [],
            "files": []
        }
        query = "SELECT name FROM Directories WHERE parent_id = :parent_id"
        query_parameters = {"parent_id": directory_id}
        cursor.execute(query, query_parameters)
        query_results = cursor.fetchall()
        for query_result in query_results:
            results["directories"].append(query_result[0])

        query = "SELECT name FROM Files WHERE directory_id = :directory_id"
        query_parameters = {"directory_id": directory_id}
        cursor.execute(query, query_parameters)
        query_results = cursor.fetchall()
        for query_result in query_results:
            results["files"].append(query_result[0])

    cursor.close()
    conn.close()

    return results

def create_directory(virtual_path, name):
    conn = db_connect(db_filename)
    if conn is None:
        return None

    conn.execute("PRAGMA foreign_keys = ON")
    cursor = conn.cursor()

    result = None
    directory_id = get_directory_id(virtual_path, cursor)

    if directory_id is not None:
        try:
            query = "INSERT INTO Directories (parent_id, name) VALUES (:parent_id, :name) RETURNING *"
            query_parameters = {"parent_id": directory_id, "name": name}
            cursor.execute(query, query_parameters)
            result = cursor.fetchone()
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error - {e}")
            result = None

    cursor.close()
    if result is not None: conn.commit()
    conn.close()

    return result

def modify_directory(virtual_path, old_name, new_name):
    conn = db_connect(db_filename)
    if conn is None:
        return None

    cursor = conn.cursor()

    result = None
    directory_id = get_directory_id(virtual_path, cursor)

    if directory_id is not None:
        try:
            query = """
                UPDATE Directories
                SET name = :new_name
                WHERE parent_id = :parent_id and name = :old_name
                RETURNING *
            """
            query_parameters = {
                "new_name": new_name,
                "old_name": old_name,
                "parent_id": directory_id
            }
            cursor.execute(query, query_parameters)
            query_results = cursor.fetchall()
            if len(query_results) == 1:
                result = query_results[0]
        except sqlite3.IntegrityError as e:
            print(f"Integrity Error - {e}")
            result = None

    cursor.close()
    if result is not None: conn.commit()
    conn.close()

    return result


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