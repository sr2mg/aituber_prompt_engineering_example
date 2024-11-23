from pydantic import BaseModel
from openai_adapter import OpenAIAdapter


class Tweet(BaseModel):
    theme: str
    tweet: str


if __name__ == "__main__":
    system_prompt = open("storage/tweet_daily_prompt_001.txt",
                         "r", encoding="utf-8").read()
    adapter = OpenAIAdapter()
    user_prompt = "テーマ：日常"
    messages = [adapter.create_message(
        "system", system_prompt), adapter.create_message("user", user_prompt)]
    res = adapter.create_structured_output(messages, Tweet)
    print(res)
