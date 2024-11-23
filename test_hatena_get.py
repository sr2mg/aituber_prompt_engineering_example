import feedparser
import requests
from requests.auth import HTTPBasicAuth
import os
import dotenv

dotenv.load_dotenv()

hatena_id = os.getenv("HATENA_ID")
blog_id = os.getenv("HATENA_BLOG_ID")
url = f"https://blog.hatena.ne.jp/{hatena_id}/{blog_id}.hatenablog.com/atom"
key = os.getenv("HATENA_KEY")
# /entryエンドポイントを使用してデータを取得するための変数を設定
endpoint = "/entry"
req_endpoint = f"{url}{endpoint}"
# GETリクエストを送信
response = requests.get(req_endpoint,
                        auth=HTTPBasicAuth(hatena_id, key),
                        headers={'Content-Type': 'application/xml'})

if response.status_code == 200:
    print("ok")
else:
    print(f'Failed to get data: {response.status_code}')
    exit(1)
response_xml = response.text
print(response_xml)


# レスポンスのXMLをパースして、記事のタイトルとURLを取得
feed = feedparser.parse(response_xml)

# ブログタイトル作成
print(feed)
# 型を確認
print(type(feed))
blog_title = feed.feed.title
feed_number = len(feed.entries)
print(f'Blog Title: {blog_title}')
print(f'Feed Number: {feed_number}')
