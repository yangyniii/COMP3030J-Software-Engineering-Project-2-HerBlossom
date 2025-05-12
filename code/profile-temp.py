from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
db = SQLAlchemy(app)

# 示例 User 模型，avatar 字段存储头像二进制数据
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    avatar = db.Column(db.LargeBinary, nullable=True)  # 头像二进制数据
    avatar_filename = db.Column(db.String(128), nullable=True)  # 可选，存储文件名

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def get_current_user():
    # 示例：假设当前用户为 id=1
    return User.query.get(1)

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user = get_current_user()
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_data = file.read()
            # 保存头像数据到数据库
            user.avatar = file_data
            user.avatar_filename = filename
            db.session.commit()
            flash('Avatar uploaded successfully')
            # 上传成功后重定向或返回 JSON 数据（视具体业务而定）
            return redirect(url_for('profile'))
        else:
            flash('File type not allowed')
            return redirect(request.url)
    # GET 请求时渲染模板
    return render_template('profile.html', user=user, avatar_url=user.avatar_filename or '../static/images/default_avatar.jpg')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
