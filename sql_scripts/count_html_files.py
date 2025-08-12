import os
import re

def get_ids_from_html_files():
    # 定义目标文件夹路径
    target_dir = os.path.join("templates","magazine", "magazine_contents")
    
    # 检查文件夹是否存在
    if not os.path.exists(target_dir):
        print(f"错误：文件夹 '{target_dir}' 不存在")
        return []
    
    if not os.path.isdir(target_dir):
        print(f"错误：'{target_dir}' 不是一个文件夹")
        return []
    
    # 正则表达式模式：匹配纯数字+.html的文件名
    pattern = re.compile(r'^\d+\.html$')
    
    # 存储提取的id列表
    ids = []
    
    # 遍历文件夹中的所有文件
    for filename in os.listdir(target_dir):
        file_path = os.path.join(target_dir, filename)
        if os.path.isfile(file_path) and pattern.match(filename):
            # 提取文件名中的数字部分（去掉.html后缀）
            # 方法1：使用字符串替换
            # id_str = filename.replace(".html", "")
            
            # 方法2：使用正则提取（更稳妥，避免文件名中包含多个.的情况）
            id_str = re.match(r'^(\d+)\.html$', filename).group(1)
            
            # 转换为整数并添加到列表
            ids.append(int(id_str))
    
    return ids

if __name__ == "__main__":
    id_list = get_ids_from_html_files()
    print(f"提取到的id列表：{id_list}")
    print(f"id数量：{len(id_list)}")
