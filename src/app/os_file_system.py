import os

CHUNK_SIZE = 1024

def os_get_file(uuid):
    dirname = os.path.dirname(__file__)
    store_path = os.path.join(dirname, f"../../storage/{uuid}")
    result = None
    print(store_path)
    try:
        with open(store_path, "rb") as file:
            result = file.read()
    except FileNotFoundError:
        print("File Content Missing")
    return result
        

def os_create_file(uuid, content):
    dirname = os.path.dirname(__file__)
    store_path = os.path.join(dirname, f"../../storage/{uuid}")
    result = True
    try:
        with open(store_path, "xb") as file:
            file.write(content)
    except FileExistsError:
        print("Duplicated uuid generated")
        result = False

    return result


def os_modify_file(uuid, content):
    pass

def os_delete_file(uuid):
    dirname = os.path.dirname(__file__)
    store_path = os.path.join(dirname, f"../../storage/{uuid}")
    try:
        os.remove(store_path)
    except FileNotFoundError:
        print("File Content Doesn't Exist")
    except:
        print("Something Went Wrong")