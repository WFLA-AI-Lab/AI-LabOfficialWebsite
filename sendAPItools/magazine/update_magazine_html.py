import requests
import os

API_ENDPOINT_PREFIX = 'http://ai-lab.club/api/magazine/update/'
API_PASSWORD = os.environ.get("AILAB_API_PWD", "ailab_api_pwd")  # 从环境变量获取，提供默认值
API_PASSWORD = "ailab_api_pwd"  # 从环境变量获取，提供默认值

def update_magazine_file(magazine_id, file_path):
    """
    向更新API发送请求以更新指定ID的杂志HTML文件
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return

    api_url = f"{API_ENDPOINT_PREFIX}{magazine_id}"
    headers = {'Authorization': API_PASSWORD}
    
    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'text/html')}
        try:
            response = requests.post(api_url, files=files, headers=headers)
            response.raise_for_status()  # 如果请求失败，抛出HTTPError
            print(f"杂志 ID {magazine_id} 的HTML文件更新请求成功！")
            print("API 响应:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"更新杂志 ID {magazine_id} 时发生错误: {e}")
            if response is not None:
                print("API 错误响应:", response.text)

if __name__ == '__main__':
    # 示例用法
    # 请将 '1' 替换为你要更新的杂志ID
    magazine_id_to_update = input("请输入要更新的杂志ID: ")
    html_file_to_send = input("请输入要发送的HTML文件路径: ")
    try:
        magazine_id_to_update = int(magazine_id_to_update)
        update_magazine_file(magazine_id_to_update, html_file_to_send)
    except ValueError:
        print("无效的杂志ID，请输入一个整数。")