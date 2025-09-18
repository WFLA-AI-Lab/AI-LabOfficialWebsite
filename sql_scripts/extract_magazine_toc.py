import os
import json
import re
import sys
import sqlite3
import os
from bs4 import BeautifulSoup
from count_html_files import get_ids_from_html_files

# 添加项目根目录到系统路径，以便导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'ailab.db')

# 社刊HTML文件目录
MAGAZINE_CONTENTS_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    'templates', 'magazine', 'magazine_contents'
)

def extract_data_from_html(html_file_path):
    """
    从HTML文件中提取杂志数据
    返回格式: {
        'title': '',
        'description': '',
        'file_path': '',
        'content_path': '',
        'author': '',
        'read_time': '',
        'toc': {}
    }
    """
    with open(html_file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # 提取标题
    title = soup.find('h1').text.strip() if soup.find('h1') else ''
    
    # 提取描述
    description = soup.find('div', 'article-summary').find('p').text.strip() if soup.find('div', 'article-summary').find('p').text.strip() else ''
    
    # 提取作者
    author = soup.find('span', id='author').text.strip() if soup.find('span', id='author') else ''
    author = author.split(":", 1)[1].strip()

    published_at = soup.find('span', id='published_at').text.strip() if soup.find('span', id='published_at') else ''
    print(published_at)
    print(bool(published_at))
    published_at = published_at.split(":", 1)[1].strip()
    # 提取阅读时间
    read_time = soup.find('span', id='read_time').text.strip() if soup.find('span', id='read_time').text.strip() else ''
    read_time = read_time.split(": ", 1)[1].strip()
    # 提取目录
    toc_dict = {}
    toc_list = soup.select('.toc-list')

    is_selcted = title.startswith("精选：")
    if toc_list:
        for toc_item in toc_list[0].find_all('a', class_='toc-link'):
            section_name = toc_item.text.strip()
            anchor_link = toc_item.get('href')
            if anchor_link and section_name:
                toc_dict[section_name] = anchor_link
    update = {
        'title': title,
        'description': description,
        'file_path': html_file_path,
        'published_at': published_at,
        'content_path': html_file_path,
        'author': author,
        'read_time': read_time,
        'toc': toc_dict,
        'is_selected':is_selcted,
    }
    return update

def update_magazine_data_in_db():
    """
    更新数据库中所有社刊的数据信息
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 获取所有社刊记录
    cursor.execute("SELECT id FROM magazine")
    magazine_db_ids = [row[0] for row in cursor.fetchall()]
    magazine_file_ids = get_ids_from_html_files()
    missing_ids =set(magazine_file_ids) - set(magazine_db_ids)
    
    for magazine_id in missing_ids:
        # 构建HTML文件路径
        html_file_path = os.path.join(MAGAZINE_CONTENTS_DIR, f"{magazine_id}.html")
        
        if os.path.exists(html_file_path):
            # 提取数据
            data = extract_data_from_html(html_file_path)
            print(bool(data))
            # 更新数据库
            try:
                # 检查记录是否存在
                cursor.execute("SELECT id FROM magazine WHERE id = ?", (magazine_id,))
                existing_record = cursor.fetchone()

                if existing_record:
                    # 如果记录存在，执行UPDATE
                    cursor.execute("""
                        UPDATE magazine SET
                            title = ?,
                            published_at = ?,
                            description = ?,
                            file_path = ?,
                            content_path = ?,
                            author = ?,
                            read_time = ?,
                            toc = ?,
                            is_selected = ?
                        WHERE id = ?
                    """, (
                        data['title'],
                        data['published_at'],
                        data['description'],
                        data['file_path'],
                        data['content_path'],
                        data['author'],
                        data['read_time'],
                        json.dumps(data['toc'], ensure_ascii=False),
                        data['is_selected'],
                        magazine_id,
                    ))
                    print(f"已更新社刊 ID {magazine_id} 的记录")
                else:
                    # 如果记录不存在，执行INSERT
                    cursor.execute("""
                        INSERT INTO magazine (
                            id, title, published_at, description, file_path, 
                            content_path, author, read_time, toc, is_selected
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        magazine_id,
                        data['title'],
                        data['published_at'],
                        data['description'],
                        data['file_path'],
                        data['content_path'],
                        data['author'],
                        data['read_time'],
                        json.dumps(data['toc'], ensure_ascii=False),
                        data['is_selected'],
                    ))
                    print(f"已添加社刊 ID {magazine_id} 的记录")
            except sqlite3.IntegrityError:
                print(f"警告：数据库访问失败, 对Magazine ID {magazine_id} 的UPDATE/INSERT操作失败。")    
        else:
            print(f"警告: Magazine ID {magazine_id} 的HTML文件不存在: {html_file_path}")
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("所有社刊数据更新完成")

if __name__ == "__main__":
    update_magazine_data_in_db()
    extract_data_from_html('C:/Users/lixiaorui/Desktop/AI lab 25/myweb/AI-LabOfficialWebsite/templates/magazine/magazine_contents/4.html')