import os, requests
def send_html_file(file_path, API_ENDPOINT,API_PASSWORD):
    """
    向API发送HTML文件
    """
    if not os.path.exists(file_path):
        print(f"错误: 文件不存在: {file_path}")
        return

    with open(file_path, 'rb') as f:
        files = {'file': (os.path.basename(file_path), f, 'text/html')}
        headers = {'Authorization': API_PASSWORD}
        
        try:
            response = requests.post(API_ENDPOINT, files=files, headers=headers)
            response.raise_for_status()  # 如果请求失败，抛出HTTPError
            print(f"文件 '{file_path}' 发送成功！")
            print("API 响应:", response.json())
        except requests.exceptions.RequestException as e:
            print(f"发送文件时发生错误: {e}")
            if response is not None:
                print("API 错误响应:", response.text)

if __name__ == '__main__':
    # 示例用法
    # 请将 'path/to/your/magazine.html' 替换为你要发送的HTML文件的实际路径
    html_file_to_send = '2123.html'
    send_html_file(html_file_to_send)