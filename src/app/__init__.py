from flask import Flask

from .directory_routes import directories_bp
from .file_routes import files_bp

app = Flask(__name__)
app.register_blueprint(directories_bp)
app.register_blueprint(files_bp)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"