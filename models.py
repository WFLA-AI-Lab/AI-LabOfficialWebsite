from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db  # 从extensions导入db，而非app


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(200))  # 存储文件路径
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'file_path': self.file_path,
            'is_published': self.is_published,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


class Magazine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    is_selected = db.Column(db.Boolean, nullable=False)  # 期号
    description = db.Column(db.Text)  # 摘要（替代原 abstract）
    file_path = db.Column(db.String(200))  # 社刊封面/附件路径（保留）
    content_path = db.Column(db.String(200), nullable=False)  # 新增：正文HTML文件路径
    # published_at = db.Column(db.DateTime, default=datetime.utcnow)
    published_at = db.Column(db.String(150), nullable=False)  # 发布日期（字符串格式）
    author = db.Column(db.String(100))  # 作者
    read_time = db.Column(db.String(20))  # 阅读时间
    toc = db.Column(db.Text)  # 存储目录的JSON字符串

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'is_selected': self.is_selected,
            'description': self.description,
            'content_path': self.content_path,  # 返回HTML路径
            'published_at': self.published_at,
            'author': self.author,
            'read_time': self.read_time,
            'toc': self.toc  # 返回目录JSON
        }


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.DateTime, nullable=False)  # 活动日期
    location = db.Column(db.String(100))  # 活动地点
    sign_up_link = db.Column(db.String(200))  # 报名链接

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'date': self.date.strftime('%Y-%m-%d %H:%M'),
            'location': self.location,
            'sign_up_link': self.sign_up_link
        }


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # 资源类型：教程、工具等
    description = db.Column(db.Text)
    file_path = db.Column(db.String(200))  # 资源文件路径
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'description': self.description,
            'file_path': self.file_path,
            'upload_time': self.upload_time.strftime('%Y-%m-%d')
        }


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    link = db.Column(db.String(200))  # 项目链接
    is_featured = db.Column(db.Boolean, default=False)  # 是否精选
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'link': self.link,
            'is_featured': self.is_featured,
            'created_at': self.created_at.strftime('%Y-%m-%d')
        }


class Personal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
