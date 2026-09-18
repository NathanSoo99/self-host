from flask import Blueprint, request, abort
from .virtual_file_system import get_directory

directories_bp = Blueprint("directories", __name__)

@directories_bp.route("/directories/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"])
def access_directories(subpath):
    if request.method == "GET":
        result = get_directory(subpath)
        if result is None:
            abort(404)
        return result
    elif request.method == "POST":
        return "wow a post request"
    elif request.method == "PUT":
        return "wow a put request"
    elif request.method == "DELETE":
        return "wow a delete request"