from flask import Flask
import os

dirname = os.path.dirname(__file__)
db_filename = os.path.join(dirname, '../../data/directory.db')

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello World</p>"