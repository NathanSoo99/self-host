import sqlite3
import uuid
from . import db_filename
from .database_access import db_connect
from collections import deque

def traverse_directories(directory_chain, cursor):
    current_directory = None

    # traverse path to find directory id
    for directory in directory_chain:
        query = """
            SELECT id, parent_id, name
            FROM Directories
            WHERE name = :directory
            AND (parent_id = :parent_id OR (parent_id IS NULL AND :parent_id IS NULL))
        """
        query_parameters = {
            "directory": directory,
            "parent_id": current_directory
        }
        cursor.execute(query, query_parameters)
        query_result = cursor.fetchone()
        if query_result is None:
            current_directory = None
            break
        else:
            current_directory = query_result[0]

    return current_directory

def get_directory_id(virtual_path, cursor):
    return traverse_directories(virtual_path.split("/"), cursor)

def get_file_metadata(virtual_path, cursor):
    path_parts = virtual_path.split("/")
    directory_chain = path_parts[0:-1]
    filename = path_parts[-1]
    result = None

    directory_id = traverse_directories(directory_chain, cursor)
    if directory_id is not None:
        query = "SELECT id, name, uuid FROM Files WHERE name = :filename AND directory_id = :directory_id"
        query_parameters = {"filename": filename, "directory_id": directory_id}
        cursor.execute(query, query_parameters)
        query_result = cursor.fetchone()
        if query_result is not None:
            result = {
                "id": query_result[0],
                "name": query_result[1],
                "uuid": query_result[2]
            }

    return result
    

def get_directory(virtual_path):
    conn = db_connect(db_filename)
    if conn is None:
        return None

    cursor = conn.cursor()

    directory_id = get_directory_id(virtual_path, cursor)
    results = {
        "directories": [],
        "files": []
    }

    if directory_id is not None:
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
    else:
        results = None

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


def delete_directory(virtual_path):
    conn = db_connect(db_filename)
    if conn is None:
        return None

    cursor = conn.cursor()

    result = True
    directory_id = get_directory_id(virtual_path, cursor)

    if directory_id is not None:
        directories_to_delete = []
        files_to_delete = []
        queue = deque()

        # Mark Directory, Sub-directories and Sub-files for deletion
        queue.append(directory_id)
        directories_to_delete.append(directory_id)
        while len(queue) != 0:
            node_id = queue.popleft()
            query = "SELECT id FROM Directories WHERE parent_id = :parent_id"
            query_parameters = {"parent_id": node_id}
            cursor.execute(query, query_parameters)
            query_results = cursor.fetchall()
            for query_result in query_results:
                queue.append(query_result[0])
                directories_to_delete.append(query_result[0])

            query = "SELECT id, uuid FROM Files WHERE directory_id = :parent_id"
            cursor.execute(query, query_parameters)
            query_results = cursor.fetchall()
            for query_result in query_results:
                files_to_delete.append(query_result[0])

        # Delete all marked files and directories from virtual file system
        # TODO delete actual files from disk and error rollback
        try:
            for file in files_to_delete:
                query = "DELETE FROM Files WHERE id = :file_id"
                query_parameters = {"file_id": file[0]}
                cursor.execute(query, query_parameters)
        except sqlite3.Error as e:
            print(f"An Error Occurred - {e}")
            result = False

        try:
            for directory in directories_to_delete:
                query = "DELETE FROM Directories WHERE id = :directory_id"
                query_parameters = {"directory_id": directory}
        except sqlite3.Error as e:
            print(f"An Error Occurred - {e}")
            result = False

        cursor.close()
        conn.commit()
        conn.close()
        return result



def get_file(path):
    conn = db_connect(db_filename)
    if conn is None:
        return None
    
    result = None

    cursor = conn.cursor()
    file_metadata = get_file_metadata(path, cursor)
    if file_metadata is not None:
        result = file_metadata

    cursor.close()
    conn.close()
    return result

def add_file(directory_path, filename, content):
    conn = db_connect(db_filename)
    if conn is None:
        return None
    
    result = False
    cursor = conn.cursor()
    directory_id = get_directory_id(directory_path, cursor)
    if directory_id is not None:
        file_identifier = uuid.uuid4().bytes
        # TODO write content to physical disk with file identifier
        print(content)
        query = "INSERT INTO Files (directory_id, name, uuid) VALUES (:directory_id, :name, :uuid) RETURNING *"
        query_data = {
            "directory_id": directory_id,
            "name": filename,
            "uuid": file_identifier
        }
        cursor.execute(query, query_data)
        result = True

    cursor.close()
    conn.commit()
    conn.close()

    return result


def modify_file_content(path, new_content):
    conn = db_connect(db_filename)
    if conn is None:
        return None
    
    result = False
    cursor = conn.cursor()
    file_metadata = get_file_metadata(path, cursor)
    if file_metadata is not None:
        print(new_content)
        result = True
        
    cursor.close()
    conn.commit()
    conn.close()
    return result

def modify_file_name(path, new_name):
    conn = db_connect(db_filename)
    if conn is None:
        return None
    result = False
    cursor = conn.cursor()
    file_metadata = get_file_metadata(path, cursor)
    if file_metadata is not None:
        query = """
            UPDATE Files
            SET name = :new_name
            WHERE id = :file_id
        """
        query_parameters = {
            "new_name": new_name,
            "file_id": file_metadata["id"]
        }
        cursor.execute(query, query_parameters)
    cursor.close()
    conn.commit()
    conn.close()
    return result

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