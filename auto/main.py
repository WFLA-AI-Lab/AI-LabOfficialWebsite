API_ENDPOINT = 'http://ai-lab.club/api/magazine/create'
API_PASSWORD = 'ailab_api_pwd'  # 替换为实际密码
from openai import OpenAI
import os,random,datetime,requests, make, paraphase, send, argparse
# api_key = os.environ.get('OPENAI_API_KEY')ss


parser = argparse.ArgumentParser(description="带默认值的可选参数示例")
parser.add_argument(
        '--API_KEY', 
        type=str,
        default=os.environ.get('OPENAI_API_KEY'),  # 默认值
        help='API访问密钥（默认：使用内置默认值）'
    )
args = parser.parse_args()
api_key = args.API_KEY

magazine = paraphase.extract_magazine(api_key)
rawhtml = make.convert2std(magazine, 'magazine.html')
send.send_html_file(rawhtml,API_ENDPOINT,API_PASSWORD)