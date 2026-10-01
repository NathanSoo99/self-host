from flask import Blueprint, request, abort
from .virtual_file_system import get_directory, create_directory, modify_directory, delete_directory

directories_bp = Blueprint("directories", __name__)

@directories_bp.route("/directories/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"])
def access_directories(subpath):
    if request.method == "GET":
        result = get_directory(subpath)
        if result is None:
            abort(404)
        return result
    elif request.method == "POST":
        directory_name = request.get_json().get("directory_name")
        if directory_name is not None:
            return ("success", 200) if create_directory(subpath, directory_name) is not None else ("directory creation failed", 500)
        else:
            abort(400)        
    elif request.method == "PUT":
        new_directory_name = request.get_json().get("new_name")
        if new_directory_name is not None:
            return ("success", 200) if modify_directory(subpath, new_directory_name) is not None else ("directory rename failed", 500)
        else:
            abort(400)
    elif request.method == "DELETE":
        return ("success", 200) if delete_directory(subpath) is True else ("directory deletion failed", 500)