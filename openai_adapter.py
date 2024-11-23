import os
from typing import Literal, TypedDict, Type
import dotenv
from openai import OpenAI
from pydantic import BaseModel
dotenv.load_dotenv()


class Message(TypedDict):
    role: Literal["system", "user", "assistant"]
    content: str


class OpenAIAdapter:
    MODEL_NAME = "gpt-4o"

    def __init__(self, model_name: str = MODEL_NAME):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.MODEL_NAME = model_name

    def chat_completions(self, messages: list[Message]):
        res = self.client.chat.completions.create(
            model=self.MODEL_NAME,
            messages=messages,

        )
        return res.choices[0].message.content

    def create_structured_output(
            self,
            messages: list[Message],
            response_format: Type[BaseModel],
            temperature: float = 0.8
    ) -> Type[BaseModel]:
        # NOTICE: structured_outputは古い一部モデルでは使えないため、エラーが出たら確認すること
        res = self.client.beta.chat.completions.parse(
            model=self.MODEL_NAME,
            messages=messages,
            temperature=temperature,
            response_format=response_format
        )
        answer = res.choices[0].message.parsed
        if answer is None:
            raise Exception("answer is None")
        return answer

    def create_message(self, role: Literal["system", "user", "assistant"], content: str) -> Message:
        return {"role": role, "content": content}

    def create_voice(self, text: str) -> bytes:
        res = self.client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )
        return res.content


if __name__ == "__main__":
    adapter = OpenAIAdapter()
    print(adapter.chat_completions([{"role": "system", "content": "あなたは語尾が「のじゃ」な強気なおじいちゃんです"}, {
          "role": "user", "content": "Pythonって何？"}]))

    class TestStruct(BaseModel):
        description: str
        code: str
    res: TestStruct = adapter.create_structured_output([
        {"role": "system", "content": "あなたは優秀なプログラマーです。コードの説明を一行の日本語でdescriptionに、コードをcodeに出力せよ"},
        {"role": "user", "content": "「AITuberをはじめよう！」と出力するpythonコードを書いてみてください"}], TestStruct, temperature=0.1)
    print(res)
    code: str = res.code
    print(code)
