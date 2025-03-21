# hello.py
from flask import Flask, request, jsonify, render_template

from mysql import Mysql

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Route for the registration form
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')


# Route for the registration form submission
@app.route('/register', methods=['POST'])
def register():
    data = request.json  # Get JSON data from the request
    identification = data.get('identification')
    # print(identification)
    name = data.get('name')
    # print(name)
    email = data.get('email')
    # print(email)
    password = data.get('password')
    # print(password)
    # Set the default avatar
    avatar = "static/photo/default_avatar.png"

    db = Mysql()
    ##nsjadnj
    if db.exist_log_user(email):
        return jsonify({'message': 'Email already exists'}), 400

    db.register_user(name, password, identification, email, avatar)

    return jsonify({'message': 'Registration successful'})
