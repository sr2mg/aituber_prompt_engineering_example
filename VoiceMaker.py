import json
from typing import TypedDict
import numpy as np
from openai_adapter import OpenAIAdapter
import requests
import soundfile
import io


class VoiceIO(TypedDict):
    data: np.ndarray
    sample_rate: int


class VoiceMaker:
    @staticmethod
    def make_voice_openai(text: str) -> VoiceIO:
        adapter = OpenAIAdapter()
        response_bytes = adapter.create_voice(text)
        data, sample_rate = soundfile.read(io.BytesIO(response_bytes))
        return VoiceIO(data=data, sample_rate=sample_rate)

    @staticmethod
    def make_voice_voicevox(text: str) -> VoiceIO:
        adapter = VoicevoxAdapter()
        return adapter.get_voice(text)


class VoicevoxAdapter:
    URL = 'http://127.0.0.1:50021/'
    # 二回postする。一回目で変換、二回目で音声合成

    def __init__(self) -> None:
        pass

    def __create_audio_query(self, text: str, speaker_id: int) -> json:
        item_data = {
            'text': text,
            'speaker': speaker_id,
        }
        response = requests.post(self.URL+'audio_query', params=item_data)
        return response.json()

    def __create_request_audio(self, query_data, speaker_id: int) -> bytes:
        a_params = {
            'speaker': speaker_id,
        }
        headers = {"accept": "audio/wav", "Content-Type": "application/json"}
        res = requests.post(self.URL+'synthesis', params=a_params,
                            data=json.dumps(query_data), headers=headers)
        print(res.status_code)
        return res.content

    def get_voice(self, text: str) -> VoiceIO:
        speaker_id = 59  # 「猫使ビィ」のspeaker_id。58がノーマル、59が落ち着き、60が人見知り
        query_data: json = self.__create_audio_query(
            text, speaker_id=speaker_id)
        query_data["speedScale"] = 1.0  # VOICEVOXでは 0.50 ~ 2.00の範囲で指定できる
        query_data["pitchScale"] = -0.05  # VOICEVOXでは-0.15 ~ 0.15の範囲で指定できる
        query_data["intonationScale"] = 0.90  # VOICEVOXでは 0.00 ~ 2.00の範囲で指定できる
        query_data["volumeScale"] = 1.0  # VOICEVOXでは 0.00 ~ 2.00の範囲で指定できる

        audio_bytes = self.__create_request_audio(
            query_data, speaker_id=speaker_id)
        audio_stream = io.BytesIO(audio_bytes)
        data, sample_rate = soundfile.read(audio_stream)
        return VoiceIO(data=data, sample_rate=sample_rate)


if __name__ == "__main__":
    voice_io = VoiceMaker.make_voice_voicevox("人工音声のテストです。")

    with open("test.wav", "wb") as f:
        # バイトデータとrateからwavファイルを作成
        soundfile.write(f, voice_io["data"], voice_io["sample_rate"])
