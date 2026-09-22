from flask import Blueprint, request, abort
from .virtual_file_system import get_directory, create_directory, delete_directory

directories_bp = Blueprint("directories", __name__)

@directories_bp.route("/directories/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"])
def access_directories(subpath):
    if request.method == "GET":
        result = get_directory(subpath)
        if result is None:
            abort(404)
        return result
    elif request.method == "POST":
        data = request.get_json()
        result = create_directory(subpath, data.get("directory_name"))
        print(result)
        return ("success", 200) if result is not None else ("directory creation failed", 500)
    elif request.method == "PUT":
        return "wow a put request"
    elif request.method == "DELETE":
        return ("success", 200) if delete_directory(subpath) is True else ("directory deletion failed", 500)