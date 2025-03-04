from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # 设置密码，自动生成哈希值
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # 校验密码
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
