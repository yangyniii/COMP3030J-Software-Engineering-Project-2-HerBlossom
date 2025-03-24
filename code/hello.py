# hello.py
from flask import Flask, request, jsonify, session, render_template
from mysql import Mysql
from werkzeug.utils import secure_filename
import os
import time
from datetime import datetime, timedelta

from flask import Flask, request, jsonify, session, render_template, redirect  # 导入 redirect
import bcrypt
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = '1'  # Set a random secret key


# Main page route
@app.route('/', methods=['GET'])
def enter_main():
    identification = session.get('identification')
    db = Mysql()

    if identification == 'A':
        accounts = db.get_all_users()
        return render_template('index.html', accounts=accounts)
    elif identification == 'B':
        return render_template('index.html')
    else:
        return redirect('/signin')

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


# Route for the login form
@app.route('/signin', methods=['GET'])
def show_signin_form():
    return render_template('signin.html')

# Login route
@app.route('/signin', methods=['POST'])
def sign_in():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid data format'}), 400

        email = data.get('email')
        password = data.get('password')
        identification = data.get('identification')

        if not email or not password or not identification:
            return jsonify({'message': 'All fields are required'}), 400

        db = Mysql()
        user = db.signin_user(identification, email, password)

        if not user:
            return jsonify({'message': 'Invalid email, password, or identification'}), 401

        if user['id'] in session:
            return jsonify({'message': 'Already logged in'}), 400

        # Store user information in the session
        session['identification'] = user['identification']
        session['email'] = user['email']
        session['user_id'] = user['id']
        # print("Session data:", session)  # Debugging session data

        # Redirect to main route based on identification
        return redirect('/')

    except Exception as e:
        print("An error occurred:", str(e))  # Debug message
        return jsonify({'message': 'An error occurred during login'}), 500





# Route for the form submission
@app.route('/signin', methods=['POST'])
def signin():
    data = request.json  # Get JSON data from the request
    identification = data.get('identification')
    email = data.get('email')
    password = data.get('password')

    db = Mysql()
    user = db.signin_user(identification, email, password)
    print("user", user)

    if user and user.get('is_banned'):
        remaining_time = (user.get('ban_end_time') - datetime.now()).total_seconds()
        if remaining_time > 0:
            return jsonify({
                'message': 'Login failed. Your account is temporarily banned.',
                'ban_reason': user.get('ban_reason'),
                'time_left': remaining_time
            }), 403

    avatar = db.get_avatar(email)
    user_id = db.get_user_id(email)

    if user:
        session['email'] = email
        session['avatar_url'] = avatar
        session['identification'] = user.get('identification')  # 从 user 字典中获取 identification
        session['user_id'] = user_id  # 假设 user_id 是一个元组，取第一个元素
        print("userid+", user_id)
        # print("login success")
        # print(avatar)
        return jsonify({'message': 'Login successful', 'redirect': '/profile'})
    else:
        # print("login failed")
        return jsonify({'message': 'Login failed. Please check your credentials.'})


@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear all session data
    return jsonify({'message': 'Logged out successfully'})


# Route for the registration form
@app.route('/register', methods=['GET'])
def show_register_form():
    return render_template('register.html')

# Route for guest access to the main page
@app.route('/guest', methods=['GET'])
def guest_access():
    return render_template('main.html')

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
    if db.exist_log_user(email):
        return jsonify({'message': 'Email already exists'}), 400

    db.register_user(name, password, identification, email, avatar)

    return jsonify({'message': 'Registration successful'})


# Set up the basic port for the pages
if __name__ == '__main__':
    app.run(debug=True, port=5222, host='127.0.0.1')
