from flask import Blueprint, request, abort
from .virtual_file_system import get_directory

directories_bp = Blueprint("directories", __name__)

@directories_bp.route("/directories/<path:subpath>", methods=["GET"])
def access_directories(subpath):
    if request.method == "GET":
        result = get_directory(subpath)
        if result is None:
            abort(404)
        return result
    return subpath