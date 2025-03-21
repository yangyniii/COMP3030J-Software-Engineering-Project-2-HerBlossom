# hello.py
from flask import Flask, request, jsonify, render_template

from mysql import Mysql

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
