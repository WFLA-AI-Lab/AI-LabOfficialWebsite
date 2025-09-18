API_ENDPOINT = 'http://ai-lab.club/api/magazine/create'
API_PASSWORD = 'ailab_api_pwd'  # 替换为实际密码
from openai import OpenAI
import os,random,datetime,requests, make, paraphase, send

magazine = paraphase.extract_magazine()
rawhtml = make.convert2std(magazine, 'magazine.html')
send.send_html_file(rawhtml,API_ENDPOINT,API_PASSWORD)