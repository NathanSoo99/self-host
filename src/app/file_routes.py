from flask import Blueprint, request, abort
from .virtual_file_system import get_file, add_file

files_bp = Blueprint("files", __name__)

@files_bp.route("/files/<path:subpath>", methods=["GET", "POST", "PUT", "DELETE"])
def access_files(subpath):
    if request.method == "GET":
        result = get_file(subpath)
        if result is None:
            abort(404)
        return result
    elif request.method == "POST":
        data = request.get_json()
        return ("success", 200) if add_file(subpath, data.get("filename"), data.get("file_content").encode("utf-8")) is True else ("upload failed", 500)
    elif request.method == "PUT":
        return "Wow a put request"
    elif request.method == "DELETE":
        return "Wow a delete request"