import os
import sys
import sqlite3

# 添加项目根目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 数据库路径
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'instance', 'ailab.db')

# SQL脚本路径
SQL_SCRIPT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'magazine_toc.sql')

def execute_sql_script(db_path, sql_script_path):
    """
    执行SQL脚本文件
    """
    print(f"正在执行SQL脚本: {sql_script_path}")
    
    # 读取SQL脚本内容
    with open(sql_script_path, 'r', encoding='utf-8') as f:
        sql_script = f.read()
    
    # 连接数据库并执行脚本
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 分割SQL语句并执行
    for statement in sql_script.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
                print(f"执行SQL语句成功: {statement.strip()}")
            except sqlite3.Error as e:
                print(f"执行SQL语句失败: {statement.strip()}\n错误: {e}")
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    print("SQL脚本执行完成")

def main():
    # 检查数据库文件是否存在
    if not os.path.exists(DB_PATH):
        print(f"错误: 数据库文件不存在: {DB_PATH}")
        return
    
    # 检查SQL脚本文件是否存在
    if not os.path.exists(SQL_SCRIPT_PATH):
        print(f"错误: SQL脚本文件不存在: {SQL_SCRIPT_PATH}")
        return
    
    # 执行SQL脚本
    execute_sql_script(DB_PATH, SQL_SCRIPT_PATH)
    
    # 提示用户运行提取目录的脚本
    print("\n数据库结构更新完成。")
    print("现在您可以运行 extract_magazine_toc.py 脚本来提取社刊目录并更新到数据库中。")
    print("命令: python sql_scripts/extract_magazine_toc.py")

if __name__ == "__main__":
    main()