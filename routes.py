from flask import render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
from functools import wraps
import os
import datetime
from werkzeug.utils import secure_filename
from extensions import db
from models import (
    Admin, News, Magazine, Activity, 
    Resource, Project, Personal
)
from api_handlers import handle_magazine_upload, handle_magazine_delete, handle_magazine_update


# 配置与工具函数
# ------------------------------------------------------

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'md', 'html', 'zip', 'rar'}

def allowed_file(filename):
    """检查文件是否为允许的类型"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# 权限装饰器
# ------------------------------------------------------
        
def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 验证会话中是否有管理员登录标识
        if 'admin_logged_in' not in session:
            flash('请先登录管理员账户', 'warning')
            return redirect(url_for('admin_login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


# 路由注册函数
# ------------------------------------------------------

def register_routes(app):
    """注册所有路由，接收app实例确保正确关联"""
    
    # 配置上传文件夹
    UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    # ------------------------------
    # 前台公共路由
    # ------------------------------
    
    @app.route('/')
    def index():
        """网站首页"""
        # 在应用上下文中执行数据库查询
        with app.app_context():
            latest_news_items = News.query.order_by(News.created_at.desc()).limit(2).all()
            latest_magazine_items = Magazine.query.order_by(Magazine.published_at.desc()).limit(2).all()
            featured_projects = Project.query.filter_by(is_featured=True).limit(2).all()
        
        return render_template('index.html', 
                             latest_news_items=latest_news_items,
                             latest_magazine_items=latest_magazine_items,
                             featured_projects=featured_projects)
    
    @app.route('/news')
    def news_list():
        """动态列表页"""
        with app.app_context():
            news_items = News.query.order_by(News.created_at.desc()).all()
        
        return render_template('news/list.html', news=news_items)
    
    @app.route('/news/<int:id>')
    def news_detail(id):
        """动态详情页"""
        with app.app_context():
            news_item = News.query.get_or_404(id)
            
            # 未发布内容仅管理员可见

            
            # 获取相关动态
            related_news = News.query.filter(News.id != id)\
                            .order_by(News.created_at.desc())\
                            .limit(3).all()
        
        return render_template('news/detail.html', 
                             news=news_item,
                             related_news= related_news)
    
    @app.route('/magazine')
    def magazine_list():
        """社刊列表页"""
        def to_roman(n):
            vals = [(1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')]
            roman = ''
            for value, symbol in vals:
                while n >= value:
                    roman += symbol
                    n -= value
            return roman
        with app.app_context():
            magazines_data = []
            for m in Magazine.query.order_by(Magazine.id.desc()).all():
                data = m.to_dict()
                # 将 published_at 字符串转换为 datetime 对象
                if isinstance(data['published_at'], str):
                    try:
                        data['published_at'] = datetime.datetime.strptime(data['published_at'], '%Y年%m月%d日')
                    except ValueError:
                        # 如果转换失败，设置为一个默认的 datetime 对象
                        data['published_at'] = datetime.datetime(0000, 0, 0)
                elif data['published_at'] is None:
                    # 如果是 None，也设置为一个默认的 datetime 对象
                    data['published_at'] = datetime.datetime(0000, 0, 0)

                if data['toc']:
                    try:
                        import json
                        toc_dict = json.loads(data['toc'])
                        titles = [f"{to_roman(i+1)} {title}" for i, title in enumerate(list(toc_dict.keys())[:6])]
                        formatted = []
                        for i in range(0, len(titles), 2):
                            line_content = f"<span class='toc-item'>·{titles[i]}</span>"
                            if i+1 < len(titles):
                                line_content += f"<span class='toc-item'>·{titles[i+1]}</span>"
                            formatted.append(f"<div class='toc-row'> {line_content} </div>")
                        if len(toc_dict) > 6:
                            formatted.append('·...')
                        data['formatted_toc'] = '<br>'.join(formatted)
                    except:
                        data['formatted_toc'] = ''
                else:
                    data['formatted_toc'] = ''
                magazines_data.append(data)
        return render_template('magazine/list.html', magazines=magazines_data)
    
    @app.route('/magazine/<int:id>')
    def magazine_detail(id):
        """社刊详情页"""
        with app.app_context():
            magazine = Magazine.query.get_or_404(id)
            # 如果存在目录数据，将其转换为Python字典
            toc_data = None
            if magazine.toc:
                import json
                try:
                    toc_data = json.loads(magazine.toc)
                except json.JSONDecodeError:
                    app.logger.error(f"社刊ID {id} 的目录数据格式错误")
        return render_template('magazine/detail.html', magazine=magazine, id=str(id), toc_data=toc_data)
    
    @app.route('/api/magazine/<int:id>/toc')
    def magazine_toc_api(id):
        """获取社刊目录的API"""
        with app.app_context():
            magazine = Magazine.query.get_or_404(id)
            if magazine.toc:
                import json
                try:
                    toc_data = json.loads(magazine.toc)
                    return jsonify({
                        'success': True,
                        'toc': toc_data
                    })
                except json.JSONDecodeError:
                    return jsonify({
                        'success': False,
                        'error': '目录数据格式错误'
                    }), 500
            else:
                return jsonify({
                    'success': False,
                    'error': '该社刊没有目录数据'
                }), 404

    @app.route('/api/magazine/create', methods=['POST'])
    def upload_magazine_html():
        """上传社刊HTML的API"""
        return handle_magazine_upload()

    @app.route('/api/magazine/delete/<int:magazine_id>', methods=['DELETE'])
    def delete_magazine(magazine_id):
        """删除社刊的API"""
        return handle_magazine_delete(magazine_id)

    @app.route('/api/magazine/update/<int:magazine_id>', methods=['POST'])
    def update_magazine(magazine_id):
        """更新社刊的API"""
        return handle_magazine_update(magazine_id)
    
    @app.route('/activities')
    def activity_list():
        """活动列表页"""
        now = datetime.datetime.now()
        with app.app_context():
            upcoming_activities = Activity.query.filter(Activity.date >= now)\
                                .order_by(Activity.date.asc()).all()
            past_activities = Activity.query.filter(Activity.date < now)\
                             .order_by(Activity.date.desc()).all()
        
        return render_template('activities/list.html', 
                             upcoming=upcoming_activities,
                             past=past_activities)
    
    @app.route('/resources')
    def resource_list():
        """资源列表页"""
        with app.app_context():
            # 按类型分组
            resource_types = [rt[0] for rt in db.session.query(Resource.type).distinct().all()]
            resources_by_type = {}
            
            for rtype in resource_types:
                resources_by_type[rtype] = Resource.query.filter_by(type=rtype)\
                                          .order_by(Resource.upload_time.desc()).all()
        
        return render_template('resources/list.html', resources_by_type=resources_by_type)
    
    @app.route('/personal')
    def personal_blog():
        """社长小窝页面"""
        with app.app_context():
            posts = Personal.query.order_by(Personal.created_at.desc()).all()
        return render_template('personal/list.html', posts=posts)
    
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        """提供上传文件的访问"""
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
    # ------------------------------
    # 管理员路由
    # ------------------------------
    
    @app.route('/admin/login', methods=['GET', 'POST'])
    def admin_login():
        """管理员登录"""
        if 'admin_logged_in' in session:
            return redirect(url_for('admin_dashboard'))
            
        if request.method == 'POST':
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            
            if not username or not password:
                flash('用户名和密码不能为空', 'danger')
                return render_template('admin/login.html')
                
            with app.app_context():
                admin = Admin.query.filter_by(username=username).first()
            
            if admin and admin.check_password(password):
                session['admin_logged_in'] = True
                session['admin_username'] = username
                flash('登录成功', 'success')
                return redirect(url_for('admin_dashboard'))
            else:
                flash('用户名或密码错误', 'danger')
        
        return render_template('admin/login.html')
    
    @app.route('/admin/logout')
    @admin_required
    def admin_logout():
        """管理员登出"""
        session.pop('admin_logged_in', None)
        session.pop('admin_username', None)
        flash('已成功登出', 'success')
        return redirect(url_for('index'))
    
    @app.route('/admin/dashboard')
    @admin_required
    def admin_dashboard():
        """管理员仪表盘"""
        with app.app_context():
            stats = {
                'news_total': News.query.count(),
                'news_published': News.query.filter_by(is_published=True).count(),
                'magazines': Magazine.query.count(),
                'activities': Activity.query.count(),
                'resources': Resource.query.count(),
                'projects': Project.query.count()
            }
            
            recent_news = News.query.order_by(News.created_at.desc()).limit(5).all()
        
        return render_template('admin/dashboard.html', 
                             stats=stats,
                             recent_news=recent_news)
    
    # ------------------------------
    # 动态管理 (CRUD)
    # ------------------------------
    
    @app.route('/admin/news')
    @admin_required
    def admin_news_list():
        """管理动态列表"""
        with app.app_context():
            news_items = News.query.order_by(News.created_at.desc()).all()
        return render_template('admin/news/list.html', news_items=news_items)
    
    @app.route('/admin/news/create', methods=['GET', 'POST'])
    @admin_required
    def admin_news_create():
        """创建新动态"""
        if request.method == 'POST':
            try:
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                
                if not title or not content:
                    flash('标题和内容不能为空', 'danger')
                    return render_template('admin/news/create.html')
                
                with app.app_context():
                    # 创建新动态
                    news = News(
                        title=title,
                        content=content,
                        is_published=request.form.get('is_published') == 'on',
                        created_at=datetime.datetime.now()
                    )
                    
                    # 处理文件上传
                    if 'file' in request.files:
                        file = request.files['file']
                        if file and file.filename and allowed_file(file.filename):
                            filename = secure_filename(f"news_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            news.file_path = filename
                    
                    db.session.add(news)
                    db.session.commit()
                
                flash('动态创建成功', 'success')
                return redirect(url_for('admin_news_list'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'创建失败: {str(e)}', 'danger')
        
        return render_template('admin/news/create.html')
    
    @app.route('/admin/news/<int:id>/edit', methods=['GET', 'POST'])
    @admin_required
    def admin_news_edit(id):
        """编辑动态"""
        with app.app_context():
            news = News.query.get_or_404(id)
        
        if request.method == 'POST':
            try:
                title = request.form.get('title', '').strip()
                content = request.form.get('content', '').strip()
                
                if not title or not content:
                    flash('标题和内容不能为空', 'danger')
                    return render_template('admin/news/edit.html', news=news)
                
                with app.app_context():
                    # 更新动态信息
                    news.title = title
                    news.content = content
                    news.is_published = request.form.get('is_published') == 'on'
                    
                    # 处理新文件上传
                    if 'file' in request.files:
                        file = request.files['file']
                        if file and file.filename and allowed_file(file.filename):
                            # 删除旧文件
                            if news.file_path:
                                old_path = os.path.join(app.config['UPLOAD_FOLDER'], news.file_path)
                                if os.path.exists(old_path):
                                    os.remove(old_path)
                            
                            # 保存新文件
                            filename = secure_filename(f"news_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                            news.file_path = filename
                    
                    db.session.commit()
                
                flash('动态更新成功', 'success')
                return redirect(url_for('admin_news_list'))
                
            except Exception as e:
                db.session.rollback()
                flash(f'更新失败: {str(e)}', 'danger')
        
        return render_template('admin/news/edit.html', news=news)
    
    @app.route('/admin/news/<int:id>/delete', methods=['POST'])
    @admin_required
    def admin_news_delete(id):
        """删除动态"""
        try:
            with app.app_context():
                news = News.query.get_or_404(id)
                
                # 删除关联文件
                if news.file_path:
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], news.file_path)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                
                db.session.delete(news)
                db.session.commit()
            
            flash('动态已删除', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'删除失败: {str(e)}', 'danger')
        
        return redirect(url_for('admin_news_list'))
    
    # ------------------------------
    # 社刊管理 (示例)
    # ------------------------------
    
    @app.route('/admin/magazines')
    @admin_required
    def admin_magazine_list():
        """社刊管理列表"""
        with app.app_context():
            magazines = Magazine.query.order_by(Magazine.published_at.desc()).all()
        return render_template('admin/magazine/list.html', magazines=magazines)
    
    # 其他社刊管理路由省略...
    
    # ------------------------------
    # API接口
    # ------------------------------
    
    @app.route('/api/latest-news')
    def api_latest_news():
        """获取最新动态API"""
        limit = min(request.args.get('limit', 5, type=int), 10)
        with app.app_context():
            news_items = News.query.filter_by(is_published=True)\
                        .order_by(News.created_at.desc())\
                        .limit(limit).all()
        
        return jsonify({
            'status': 'success',
            'count': len(news_items),
            'data': [item.to_dict() for item in news_items]
        })
    
    # ------------------------------
    # 错误处理
    # ------------------------------
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403
    
    return app
