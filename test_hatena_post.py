import requests
from requests.auth import HTTPBasicAuth
import dotenv
import os

dotenv.load_dotenv()

hatena_id = os.getenv("HATENA_ID")
blog_id = os.getenv("HATENA_BLOG_ID")
url = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}.hatenablog.com/atom"
key = os.getenv("HATENA_KEY")
# /entryエンドポイントを使用してデータを取得するための変数を設定
endpoint = "/entry"
req_endpoint = f"{url}{endpoint}"
# test_post_data.xmlを読み込む
with open('test_post_data.xml', 'r', encoding='utf-8') as file:
    data = file.read()

# POSTリクエストを送信
response = requests.post(req_endpoint, auth=HTTPBasicAuth(username=hatena_id, password=key), headers={'Content-Type': 'application/xml'}, data=data)

if response.status_code == 201:
    print("ok")
else:
    print(f'Failed to post: {response.status_code}')
    exit(1)