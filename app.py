from flask import Flask
import os
from extensions import db  # 从extensions导入db

# 1. 初始化Flask应用
app = Flask(__name__)

# 2. 配置数据库（必须在db.init_app前）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ailab.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # 用于session加密

# 3. 初始化数据库（关键：先关联app和db）
db.init_app(app)

# 4. 注册路由（必须在db.init_app之后）
from routes import register_routes
register_routes(app)  # 显式传入app实例

# 5. 创建数据库表（首次运行时）
with app.app_context():  # 激活应用上下文
    db.create_all()

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)