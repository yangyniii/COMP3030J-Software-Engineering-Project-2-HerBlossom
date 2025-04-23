# hello.py
from flask import Flask, request, jsonify, session, render_template
from mysql import Mysql
from werkzeug.utils import secure_filename
import time
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

        if user['email'] in session:
            return jsonify({'message': 'Already logged in'}), 400

        # Store user information in the session
        session['email'] = user['email']
        session['user_id'] = user['user_id']

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
        db.register_user(name, password, email, '../static/images/chiikawa.jpg', '../static/images/chiikawa.jpg', 0, 0, 0, 0, 0, "null", "null", "null")
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
    user_id = request.args.get('user_id')  # 从查询参数获取 user_id
    print(f"Received user_id: {user_id}")
    if not user_id:
        return jsonify({'message': 'User ID is required'}), 400  # 如果 user_id 为空，则返回 400

    db = Mysql()  # 实例化数据库对象
    user_info = db.get_user_info_by_id(user_id)  # 查询用户信息
    print('get_user_info_by_id User data:', user_info)  # 调试打印

    if not user_info:
        return jsonify({'message': 'User not found'}), 404  # 如果用户不存在，则返回 404

    # 在确认 user_info 不为空后再访问 avatar
    avatar_path = user_info.get('avatar', 'chiikawa.jpg')
    if not avatar_path.startswith('../'):
        avatar_path = '../static/images/' + avatar_path
    print('Avatar path11:', avatar_path)

    return jsonify({
        'username': user_info.get('username', ''),
        'password': user_info.get('password', ''),  # 这里最好不要返回密码
        'email': user_info.get('email', ''),
        'avatar': avatar_path  # 使用默认头像
    })




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


@app.route('/search_posts', methods=['GET'])
def search_posts():
    title = request.args.get('title', '')
    db = Mysql()
    try:
        posts = db.search_posts_by_title(title)
        return jsonify({'posts': posts})
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

    return render_template('forums.html',
                           posts=posts,
                           online_count=online_count,
                           total_posts=total_posts,
                           total_comments=total_comments,
                           hot_tags=hot_tags,
                           is_logged_in='email' in session)




@app.route('/blog-list', methods=['GET'])
def blog_list():
    return render_template('blog-list.html')

@app.route('/blog-single', methods=['GET'])
def blog_single_default():
    return render_template('blog-single.html')

@app.route('/blog', methods=['GET'])
def blog_grid():
    db = Mysql()
    # 获取特色博客
    featured_blog = db.get_featured_blog()
    # 获取所有博客
    all_blogs = db.get_all_blogs()
    
    # 将博客数据转换为字典列表，方便在模板中使用
    blogs = []
    for blog in all_blogs:
        blog_dict = {
            'blog_id': blog[0],
            'title': blog[1],
            'content': blog[2],
            'image_url': blog[3],
            'category': blog[4],
            'read_time': blog[5],
            'author_name': blog[6],
            'author_avatar': blog[7],
            'publish_date': blog[8],
            'link_url': blog[9],
            'is_featured': blog[10]
        }
        blogs.append(blog_dict)
    
    # 将特色博客转换为字典
    featured_blog_dict = None
    if featured_blog:
        featured_blog_dict = {
            'blog_id': featured_blog[0],
            'title': featured_blog[1],
            'content': featured_blog[2],
            'image_url': featured_blog[3],
            'category': featured_blog[4],
            'read_time': featured_blog[5],
            'author_name': featured_blog[6],
            'author_avatar': featured_blog[7],
            'publish_date': featured_blog[8],
            'link_url': featured_blog[9],
            'is_featured': featured_blog[10]
        }
    
    return render_template('blog.html', blogs=blogs, featured_blog=featured_blog_dict)

@app.route('/blog-category/<category>', methods=['GET'])
def blog_category(category):
    db = Mysql()
    # 获取指定分类的博客
    category_blogs = db.get_blogs_by_category(category)
    
    # 将博客数据转换为字典列表
    blogs = []
    for blog in category_blogs:
        blog_dict = {
            'blog_id': blog[0],
            'title': blog[1],
            'content': blog[2],
            'image_url': blog[3],
            'category': blog[4],
            'read_time': blog[5],
            'author_name': blog[6],
            'author_avatar': blog[7],
            'publish_date': blog[8],
            'link_url': blog[9],
            'is_featured': blog[10]
        }
        blogs.append(blog_dict)
    
    return render_template('blog.html', blogs=blogs, category=category)

@app.route('/blog-search', methods=['GET'])
def blog_search():
    keyword = request.args.get('keyword', '')
    db = Mysql()
    # 搜索博客
    search_results = db.search_blogs(keyword)
    
    # 将博客数据转换为字典列表
    blogs = []
    for blog in search_results:
        blog_dict = {
            'blog_id': blog[0],
            'title': blog[1],
            'content': blog[2],
            'image_url': blog[3],
            'category': blog[4],
            'read_time': blog[5],
            'author_name': blog[6],
            'author_avatar': blog[7],
            'publish_date': blog[8],
            'link_url': blog[9],
            'is_featured': blog[10]
        }
        blogs.append(blog_dict)
    
    return render_template('blog.html', blogs=blogs, keyword=keyword)

@app.route('/blog-single/<int:blog_id>', methods=['GET'])
def blog_single(blog_id):
    db = Mysql()
    # 获取博客详情
    blog = db.get_blog_by_id(blog_id)
    
    if blog:
        blog_dict = {
            'blog_id': blog[0],
            'title': blog[1],
            'content': blog[2],
            'image_url': blog[3],
            'category': blog[4],
            'read_time': blog[5],
            'author_name': blog[6],
            'author_avatar': blog[7],
            'publish_date': blog[8],
            'link_url': blog[9],
            'is_featured': blog[10]
        }
        return render_template('blog-single.html', blog=blog_dict)
    else:
        return render_template('404.html')

@app.route('/blog-grid-two', methods=['GET'])
def blog_grid_two():
    return render_template('blog-grid-two.html')

@app.route('/forum-topics', methods=['GET'])
def forum_topics():
    return render_template('forum-topics.html')


@app.route('/forum-single1', methods=['GET'])
def forum_single1():
    post = {
        "title": "Are there any scandal-free sanitary pad brands left?",
        "content": "The first major scandal of this year's Consumer Rights Day (March 15) was about sanitary pads. It exposed a shocking black market: discarded pads were simply rinsed, pressed back into shape, and then sold as \"brand-new\" products.  The pictures were so disgusting that words can't even describe them.  These \"recycled\" sanitary pads had bacterial levels exceeding the limit by nearly 100 times, with dangerous pathogens like E. coli and Staphylococcus aureus present in alarming amounts. Long-term use could lead to gynecological infections and even infertility. Even worse, some products contained fluorescent agents far beyond safety standards, posing a cancer risk. When women's health is compromised, the next generation suffers too.  Whether we're called \"queens,\" \"goddesses,\" or just \"women\" doesn't really matter. What matters is:  Does society respect women's biological needs? Are women's basic health concerns acknowledged, discussed, and treated without bias or neglect?  So, are there any sanitary pad brands left that haven't been exposed yet? And will women's safety ever be taken seriously?"
    }
    return render_template('forum-single1.html', post=post)  # 传递 post 变量



@app.route('/post-edit', methods=['GET', 'POST'])
def post_edit():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        category = request.form.get('category')

        # 打印数据，检查是否获取到数据
        print(f"Title: {title}, Content: {content}, Tags: {tags}, Category: {category}")

        # 处理图片上传
        image_urls = []
        image_files = request.files.getlist('images')
        print(f"Received images: {len(image_files)}")
        if not image_files:
            print("No images received.")

        # 检查图片是否成功上传
        for image in image_files:
            if image:
                filename = secure_filename(image.filename)
                image.save(os.path.join('static/uploads', filename))
                image_urls.append(f'uploads/{filename}')
                print(f"Saved image: {filename}")

        # 假设从 Session 获取用户 ID

        user_id = session.get('user_id')  # 你可以根据实际情况获取用户 ID

        # 保存到数据库
        db = Mysql()
        try:
            db.insert_post(user_id, title, content, tags, category, ','.join(image_urls))
            return jsonify({'message': 'Post saved successfully'}), 200
        except Exception as e:
            print(f"Error saving post: {e}")
            return jsonify({'message': 'An error occurred while submitting the post.'}), 500

    # 处理 GET 请求，渲染页面
    return render_template('post-edit.html')



@app.route('/post_posts', methods=['GET'])
def post_posts():
    db = Mysql()
    post_list = db.get_posts()
    if post_list:
        return jsonify({'posts': post_list})
    else:
        return jsonify({'message': 'No post found'}), 404


@app.route('/forum-single', methods=['GET'])
def forum_single():
    post_id = request.args.get('post_id')
    print("forum- single Received post_id:", post_id)
    if not post_id:
        return jsonify({'message': 'Post ID is required'}), 400

    db = Mysql()
    post = db.get_post_by_id(post_id)  # 你需要确保这个方法存在并能根据 post_id 返回数据
    print("forum- single Queried post:", post)

    if not post:
        return render_template('404.html', message="Post not found"), 404
    print("Image URLs raw:", post['image_urls'])

    return render_template('forum-single.html', post={
        'post_id': post['id'],
        'user_id': post['user_id'],
        'title': post['title'],
        'content': post['content'],
        'tags': post['tags'],
        'category': post['category'],
        'comment_count': post['comment_count'],
        'create_time': post['create_time'],
        'image_urls': post['image_urls'].split(',') if post['image_urls'] else []

    })

@app.route('/life-skills', methods=['GET'])
def life_skills():
    return render_template('life-skills.html')

@app.route('/mental-health', methods=['GET'])
def mental_health():
    return render_template('mental-health.html')

@app.route('/job-recommendation')
def job_recommendation():
    db = Mysql()
    job_list = db.get_all_jobs()
    return render_template('job-recommendation.html', job_list=job_list)

@app.route('/get_all_tags', methods=['GET'])
def get_all_tags():
    db = Mysql()
    try:
        tags = db.get_all_unique_tags()
        return jsonify({'success': True, 'tags': tags})
    except Exception as e:
        print(f"Error getting tags: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500


@app.route('/search_jobs', methods=['GET'])
def search_jobs():
    keyword = request.args.get('keyword', '')  # 从查询字符串中获取搜索关键词
    try:
        db = Mysql()
        jobs = db.search_jobs_by_keyword(keyword)
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# Set up the basic port for the pages
if __name__ == '__main__':
    app.run(debug=True, port=5222, host='127.0.0.1')
