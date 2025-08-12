from flask import request, jsonify
import os
from werkzeug.utils import secure_filename
from extensions import db
from models import Magazine
import subprocess
import sqlite3

DB_PATH = os.path.join( 'instance', 'ailab.db')

# 配置
ALLOWED_EXTENSIONS = {'html'}
API_PASSWORD = os.environ.get("AILAB_API_PWD", "ailab_api_pwd")  # 从环境变量获取，提供默认值
DELETE_API_PASSWORD = os.environ.get("AILAB_DELETE_API_PWD", "ailabtmppwd") # 从环境变量获取，提供默认值
MAGAZINE_CONTENT_DIR = os.path.join('templates', 'magazine', 'magazine_contents')


def allowed_file(filename):
    """检查文件是否为允许的类型"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def handle_magazine_upload():
    """
    处理杂志HTML文件上传API
    1. 验证密码
    2. 检查文件大小(<20MB)
    3. 生成新文件名(最大ID+1)
    4. 保存文件
    5. 执行目录提取脚本
    """
    # 验证密码
    if request.headers.get('Authorization') != API_PASSWORD:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    # 检查文件
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'File type not allowed'}), 400
    
    # 检查文件大小(20MB限制)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    if file_length > 20 * 1024 * 1024:  # 20MB
        return jsonify({'success': False, 'error': 'File too large (max 20MB)'}), 400
    
    # 确保目录存在
    os.makedirs(MAGAZINE_CONTENT_DIR, exist_ok=True)
    
    # 获取最大ID
    max_id = 0
    for filename in os.listdir(MAGAZINE_CONTENT_DIR):
        if filename.endswith('.html'):
            try:
                current_id = int(filename.split('.')[0])
                if current_id > max_id:
                    max_id = current_id
            except ValueError:
                continue
    
    # 生成新文件名
    new_filename = f"{max_id + 1}.html"
    file_path = os.path.join(MAGAZINE_CONTENT_DIR, new_filename)
    print(file)
    print(file_path)
    # 保存文件
    file.save(file_path)
    
    # 执行目录提取脚本
    try:
        subprocess.run(['python', 'sql_scripts/extract_magazine_toc.py'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({
            'success': False, 
            'error': f'Failed to extract TOC: {str(e)}'
        }), 500
    
    return jsonify({
        'success': True,
        'message': f'File saved as {new_filename} and TOC extracted',
        'file_id': max_id + 1
    })

def handle_magazine_delete(magazine_id):
    """
    处理杂志删除API
    1. 验证密码
    2. 从数据库中删除记录
    3. 删除HTML文件
    """
    # 验证密码
    if request.headers.get('Authorization') != DELETE_API_PASSWORD:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 检查杂志是否存在
        cursor.execute("SELECT id FROM magazine WHERE id = ?", (magazine_id,))
        if cursor.fetchone() is None:
            return jsonify({'success': False, 'error': 'Magazine not found'}), 404

        # 从数据库中删除记录
        cursor.execute("DELETE FROM magazine WHERE id = ?", (magazine_id,))
        conn.commit()

        # 删除HTML文件
        html_file_path = os.path.join(MAGAZINE_CONTENT_DIR, f"{magazine_id}.html")
        if os.path.exists(html_file_path):
            os.remove(html_file_path)
            print(f"已删除HTML文件: {html_file_path}")
        else:
            print(f"警告: HTML文件不存在: {html_file_path}")

        return jsonify({'success': True, 'message': f'Magazine {magazine_id} deleted successfully'})

    except sqlite3.Error as e:
        print(f"数据库操作错误: {e}")
        return jsonify({'success': False, 'error': f'Database error: {str(e)}'}), 500
    except Exception as e:
        print(f"删除操作错误: {e}")
        return jsonify({'success': False, 'error': f'Deletion error: {str(e)}'}), 500
    finally:
        if conn:
            conn.close()

def handle_magazine_update(magazine_id):
    """
    处理杂志HTML文件更新API
    1. 验证密码
    2. 检查文件大小(<20MB)
    3. 替换HTML文件
    4. 重新提取信息并更新数据库
    """
    # 验证密码
    if request.headers.get('Authorization') != API_PASSWORD:
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    
    # 检查文件
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'success': False, 'error': 'No selected file'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'success': False, 'error': 'File type not allowed'}), 400
    
    # 检查文件大小(20MB限制)
    file.seek(0, os.SEEK_END)
    file_length = file.tell()
    file.seek(0)
    if file_length > 20 * 1024 * 1024:  # 20MB
        return jsonify({'success': False, 'error': 'File too large (max 20MB)'}), 400
    
    # 确保目录存在
    os.makedirs(MAGAZINE_CONTENT_DIR, exist_ok=True)
    
    # 检查文件是否存在
    html_file_path = os.path.join(MAGAZINE_CONTENT_DIR, f"{magazine_id}.html")
    if not os.path.exists(html_file_path):
        return jsonify({'success': False, 'error': f'Magazine HTML file {magazine_id}.html not found'}), 404

    # 保存文件，覆盖原有文件
    file.save(html_file_path)
    
    # 执行目录提取脚本，更新数据库
    try:
        subprocess.run(['python', 'sql_scripts/extract_magazine_toc.py'], check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({
            'success': False, 
            'error': f'Failed to extract TOC: {str(e)}'
        }), 500
    
    return jsonify({
        'success': True,
        'message': f'Magazine {magazine_id}.html updated and TOC re-extracted'
    })