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
        return render_template('signin.html')
    else:
        return redirect('/signin')


@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


# Route for the login form
@app.route('/signin', methods=['GET'])
def show_signin_form():
    return render_template('signin.html')


@app.route('/index', methods=['GET'])
def show_index():
    return render_template('index.html')


# Login route
@app.route('/signin', methods=['POST'])
def sign_in():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'message': 'Invalid data format'}), 400

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return jsonify({'message': 'All fields are required'}), 400

        db = Mysql()
        user = db.signin_user(email, password)

        if not user:
            return jsonify({'message': 'Invalid email, password, or identification'}), 401

        if user['id'] in session:
            return jsonify({'message': 'Already logged in'}), 400

        # Store user information in the session
        session['email'] = user['email']
        session['user_id'] = user['id']
        print("Session data:", session)  # Debugging session data

        # Redirect to main route
        return redirect('/index')

    except Exception as e:
        print("An error occurred:", str(e))  # Debug message
        return jsonify({'message': 'An error occurred during login'}), 500


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
    return render_template('index.html')


# Route for the registration form submission
@app.route('/register', methods=['POST'])
def register():
    data = request.json  # 获取请求的 JSON 数据
    print(f"Received data: {data}")  # 打印接收到的数据
    # 检查是否包含必需字段
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Missing required fields'}), 400

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    db = Mysql()
    if db.exist_log_user(email):
        return jsonify({'message': 'Email already exists'}), 400

    try:
        db.register_user(name, password, email, 'default.jpg', 'default.jpg', 0, 0, 0, 0, 0, "null", "null", "null")
        return jsonify({'message': 'Registration successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/check_email', methods=['POST'])
def check_email():
    data = request.json
    email = data.get('email')

    db = Mysql()
    exists = db.exist_log_user(email)

    return jsonify({'exists': exists})


# Avatar-related methods

# Configure upload folder
UPLOAD_FOLDER = 'static/photo/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Add allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


# Function to check allowed extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Show the user's profile
@app.route('/profile', methods=['GET'])
def profile():
    # Check if the user is logged in
    if 'email' not in session:
        # If not logged in, return 401 error
        return render_template('signin.html')

    # print("email", session)
    # Render the Profile page
    return render_template('profile.html')


@app.route('/get_user_info', methods=['GET'])
def get_user_info():
    db = Mysql()  # Instantiate the database object
    user_email = session.get('email')  # Get the current user's email from the session
    user_info = db.get_user_info(user_email)  # Query user information from the database

    if user_info:
        # print("Fetched user info:", user_info)
        # Return user information as JSON
        return jsonify({
            'name': user_info['name'],
            'password': user_info['password'],  # Original password is used only on the backend, hide it on the frontend
            'email': user_info['email'],
            'avatar': user_info.get('avatar')
        })
    else:
        # If user is not found, return 404
        return jsonify({'message': 'User not found'}), 404


@app.route('/get_user_info_by_id', methods=['GET'])
def get_user_info_by_id():
    user_id = request.args.get('user_id')  # Get user_id from query parameter
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400  # Optional: Return an error if no user_id is provided

    db = Mysql()  # Instantiate the database object
    user_info = db.get_user_info_by_id(user_id)  # Query user information from the database

    if user_info:
        return jsonify({
            'username': user_info['username'],
            'password': user_info['password'],  # Original password is used only on the backend, hide it on the frontend
            'email': user_info['email'],
            'avatar': user_info.get('avatar')
        })
    else:
        # If user is not found, return 404
        return jsonify({'message': 'User not found'}), 404


# Handle avatar upload
@app.route('/upload_avatar', methods=['POST'])
def upload_avatar():
    # Check if the 'file' field exists in the request.files dictionary
    # If it doesn't, return a 400 Bad Request error message
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    if file and allowed_file(file.filename):
        # Generate the filename
        filename = secure_filename(file.filename)
        # Save into the database
        relative_path = f'static/photo/{filename}'
        # Save the uploaded file in the photo directory
        absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        # Ensure the directory exists
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        # Save the file
        file.save(absolute_path)

        # Get the user's email from the session
        user_email = session.get('email')
        if not user_email:
            return jsonify({'message': 'Please sign in first'}), 403

        # Update the profile picture path (relative path) in the database
        db = Mysql()
        db.update_user_avatar(user_email, relative_path)

        session['avatar_url'] = absolute_path  # Save the updated avatar in the session

        # Return success message and profile picture path (for direct use by the frontend)
        return jsonify({'message': 'Avatar uploaded successfully', 'avatar_url': f'/{relative_path}'}), 200

    return jsonify({'message': 'File not allowed'}), 400


# Update password
@app.route('/profile', methods=['POST'])
def update_password():
    new_password = request.json.get('password')
    email = session.get('email')  # Get the email from the session
    db = Mysql()
    db.update_password(email, new_password)
    return jsonify({'message': 'Password updated successfully'})


@app.route('/publish_post', methods=['GET'])
def publish_post():
    data = request.json  # 获取请求的 JSON 数据
    print(f"Received data: {data}")  # 打印接收到的数据
    # 检查是否包含必需字段
    if not data.get('user_id') or not data.get('title') or not data.get('content') or not data.get('create_time'):
        return jsonify({'message': 'Missing required fields'}), 400

    user_id = data.get('user_id')
    title = data.get('title')
    content = data.get('content')
    create_time = data.get('create_time')

    db = Mysql()

    try:
        db.publish_post(user_id, title, content, create_time)
        return jsonify({'message': 'Registration successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/delete_post', methods=['DELETE'])
def delete_post():
    post_id = request.args.get('post_id', '')
    db = Mysql()
    try:
        success = db.delete_post(post_id)
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'success': False, 'message': 'Failed to delete lost information'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/post_post', methods=['GET'])
def post_post():
    db = Mysql()
    post_list = db.get_posts()
    if post_list:
        return jsonify({'posts': post_list})
    else:
        return jsonify({'message': 'No books found'}), 404


@app.route('/publish_comment', methods=['GET'])
def publish_comment():
    data = request.json  # 获取请求的 JSON 数据
    print(f"Received data: {data}")  # 打印接收到的数据
    # 检查是否包含必需字段
    if not data.get('commentable_id') or not data.get('commentable_type') or not data.get('user_id') or not data.get(
            'content') or not data.get('create_time'):
        return jsonify({'message': 'Missing required fields'}), 400

    commentable_id = data.get('commentable_id')
    commentable_type = data.get('commentable_type')
    user_id = data.get('user_id')
    content = data.get('content')
    create_time = data.get('create_time')

    db = Mysql()

    try:
        db.publish_comment(commentable_id, commentable_type, user_id, content, create_time)
        return jsonify({'message': 'Registration successful'}), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


@app.route('/search_topics', methods=['GET'])
def search_topics():
    name = request.args.get('name', '')
    db = Mysql()
    try:
        topics = db.search_topics_by_name(name)
        return jsonify({'topics': topics})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


@app.route('/forum', methods=['GET'])
def forum():
    try:
        db = Mysql()
        # 获取帖子列表
        posts = db.get_posts()
        # 获取在线人数（这里暂时设置为固定值，后续可以改为动态计算）
        online_count = 100
        # 获取总帖子数
        total_posts = len(posts) if posts else 0
        # 获取总评论数（需要从数据库获取）
        total_comments = 0
        # 获取热门标签（需要从数据库获取）
        hot_tags = []
    except Exception as e:
        print(f"数据库连接错误: {str(e)}")
        # 设置默认值
        posts = []
        online_count = 0
        total_posts = 0
        total_comments = 0
        hot_tags = []

    return render_template('forum.html',
                           posts=posts,
                           online_count=online_count,
                           total_posts=total_posts,
                           total_comments=total_comments,
                           hot_tags=hot_tags,
                           is_logged_in='email' in session)


@app.route('/forum-single', methods=['GET'])
def post_detail():
    post_id = 1
    if post_id:
        db = Mysql()
        post = db.get_post_by_id(post_id)
        if post:
            return render_template('forum-single.html', post=post)
        else:
            return jsonify({'message': 'Post not found'}), 404
    else:
        return jsonify({'message': 'Post ID is required'}), 400

@app.route('/blog-list', methods=['GET'])
def blog_list():
    return render_template('blog-list.html')

@app.route('/blog-single', methods=['GET'])
def blog_single():
    return render_template('blog-single.html')

@app.route('/blog-grid', methods=['GET'])
def blog_grid():
    return render_template('blog-grid.html')

@app.route('/blog-grid-two', methods=['GET'])
def blog_grid_two():
    return render_template('blog-grid-two.html')

# Set up the basic port for the pages
if __name__ == '__main__':
    app.run(debug=True, port=5222, host='127.0.0.1')
