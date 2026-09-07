from flask import Blueprint, request, abort
from .virtual_file_system import get_file

files_bp = Blueprint("files", __name__)

@files_bp.route("/files/<path:subpath>", methods=["GET"])
def access_files(subpath):
    if request.method == "GET":
        result = get_file(subpath)
        if result is None:
            abort(404)
        return result