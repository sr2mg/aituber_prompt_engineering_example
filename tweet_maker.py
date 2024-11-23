import os
import random
from pydantic import BaseModel
from openai_adapter import OpenAIAdapter
from dotenv import load_dotenv
import tweepy

load_dotenv()


class Tweet(BaseModel):
    theme: str
    tweet: str


class TweetMaker:
    # このファイルのディレクトリパス
    FILE_PATH = os.path.dirname(__file__)

    def __init__(self):
        consumer_key = os.environ.get("CONSUMER_KEY")
        consumer_secret = os.environ.get("CONSUMER_SECRET")
        bearer_token = os.environ.get("BEARER_TOKEN")
        access_token = os.environ.get("ACCESS_TOKEN")
        access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")
        # APIインスタンスの作成
        self.client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                                    bearer_token=bearer_token, access_token=access_token, access_token_secret=access_token_secret)
        self.adapter = OpenAIAdapter()
        pass

    def __create_tweet_text(self) -> Tweet:
        system_prompt = open(
            self.FILE_PATH+"/storage/make_daily_tweet_prompt.txt", "r", encoding="utf-8").read()
        theme = self.__select_theme()
        user_prompt = f"テーマ：{theme}"
        messages = [self.adapter.create_message(
            "system", system_prompt), self.adapter.create_message("user", user_prompt)]
        res: Tweet = self.adapter.create_structured_output(messages, Tweet)
        return res

    def __select_theme(self) -> str:
        themes: list[str] = open(
            self.FILE_PATH+"/storage/tweet_theme.txt", "r", encoding="utf-8").readlines()
        return random.choice(themes)

    def post(self):
        tweet = self.__create_tweet_text()
        self.__post_tweet(tweet)
        return tweet

    def get_created_tweet(self) -> str:
        tweet = self.__create_tweet_text()
        return tweet.tweet

    def __post_tweet(self, tweet: Tweet):
        try:
            self.client.create_tweet(text=tweet.tweet)
            print("ポストの投稿に成功しました！")
        except tweepy.TweepError as e:
            print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    maker = TweetMaker()
    # tweet = maker.get_created_tweet()
    # print(tweet)
    tweet = maker.post()
    print("以下をポストしました...\n"+tweet.tweet)
