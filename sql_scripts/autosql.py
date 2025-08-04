import sqlite3
import os
import logging
from datetime import datetime

# 配置日志（记录执行结果，便于排查问题）
logging.basicConfig(
    filename='sql_auto_exec.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def execute_sql_from_file(db_path, sql_file):
    """从SQL文件读取并执行语句"""
    try:
        # 连接数据库
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 读取SQL文件内容
        with open(sql_file, 'r', encoding='utf-8') as f:
            sql_script = f.read()
        
        # 执行SQL（支持多语句，用分号分隔）
        cursor.executescript(sql_script)
        conn.commit()
        logging.info(f"成功执行SQL文件：{sql_file}")
        print(f"[{datetime.now()}] SQL执行成功")
        
    except Exception as e:
        conn.rollback()  # 出错时回滚
        logging.error(f"执行失败：{str(e)}", exc_info=True)
        print(f"[{datetime.now()}] 执行失败：{str(e)}")
    
    finally:
        if conn:
            conn.close()  # 确保连接关闭

if __name__ == '__main__':
    # 配置路径（根据实际项目修改）
    DB_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),  # 向上两级到根目录
        'instance', 
        'ailab.db'
    )
    SQL_FILE = os.path.join(os.path.dirname(__file__), 'auto_sql_scripts.sql')  # SQL脚本路径
    
    # 执行SQL
    execute_sql_from_file(DB_PATH, SQL_FILE)