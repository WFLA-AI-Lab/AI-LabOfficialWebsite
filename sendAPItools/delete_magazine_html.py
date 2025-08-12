import requests
import os

API_ENDPOINT_PREFIX = 'http://ai-lab.club/api/magazine/delete/'
DELETE_API_PASSWORD = os.environ.get("AILAB_DELETE_API_PWD", "ailabtmppwd") # 从环境变量获取，提供默认值

def delete_magazine_file(magazine_id):
    """
    向删除API发送请求以删除指定ID的杂志
    """
    api_url = f"{API_ENDPOINT_PREFIX}{magazine_id}"
    headers = {'Authorization': DELETE_API_PASSWORD}
    
    try:
        response = requests.delete(api_url, headers=headers)
        response.raise_for_status()  # 如果请求失败，抛出HTTPError
        print(f"Magazine ID {magazine_id} 删除请求成功！")
        print("API 响应:", response.json())
    except requests.exceptions.RequestException as e:
        print(f"删除Magazine ID {magazine_id} 时发生错误: {e}")
        if response is not None:
            print("API 错误响应:", response.text)

if __name__ == '__main__':
    # 示例用法
    # 请将 '1' 替换为你要删除的杂志ID
    magazine_id_to_delete = input("请输入要删除的杂志ID: ")
    try:
        magazine_id_to_delete = int(magazine_id_to_delete)
        delete_magazine_file(magazine_id_to_delete)
    except ValueError:
        print("无效的Magazine ID，请输入一个整数。")