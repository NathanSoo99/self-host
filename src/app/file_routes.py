from flask import Blueprint, request, abort
from .virtual_file_system import get_file, add_file, modify_file_content, modify_file_name, delete_file

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
        data = request.get_json()
        return ("success", 200) if modify_file_content(subpath, data.get("new_content")) is True else ("update failed", 500)
    elif request.method == "DELETE":
        return ("success", 200) if delete_file(subpath) is True else ("delete failed", 500)

@files_bp.route("/files/metadata/<path:subpath>", methods=["PUT"])
def access_files_metadata(subpath):
    if request.method == "GET":
        return "wow a get request"
    elif request.method == "PUT":
        data = request.get_json()
        return ("success", 200) if modify_file_name(subpath, data.get("new_name")) is True else ("update failed", 500)