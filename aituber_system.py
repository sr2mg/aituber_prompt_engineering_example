import os
from talker import Talker
from obs_adapter import OBSAdapter
from VoiceMaker import VoiceIO, VoiceMaker
from youtube_comment_adapter import YoutubeCommentAdapter
from play_sound import PlaySound
from dotenv import load_dotenv
import time
load_dotenv(override=True)


class AITuberSystem:
    def __init__(self):
        self.talker = Talker()
        self.obs_adapter = OBSAdapter()
        self.voice_maker = VoiceMaker()
        self.youtube_comment_adapter = YoutubeCommentAdapter(
            os.environ.get("YOUTUBE_VIDEO_ID"))
        self.play_sound = PlaySound()

    def start(self):
        while True:
            comment = self.youtube_comment_adapter.get_comment()
            if comment is None:
                # おとぎ話を話す
                talk = self.talker.generate_fairy_tale()
                talk_list = self.split_text(talk)
                for talk in talk_list:
                    voice: VoiceIO = self.voice_maker.make_voice_voicevox(talk)
                    self.obs_adapter.set_question("")
                    self.obs_adapter.set_answer(talk)
                    self.play_sound.play_sound(voice)
            else:
                character_speak = self.talker.chat(comment)
                speak_list = self.split_text(character_speak)
                for speak in speak_list:
                    voice: VoiceIO = self.voice_maker.make_voice_voicevox(
                        speak)
                    self.obs_adapter.set_question(comment)
                    self.obs_adapter.set_answer(speak)
                    self.play_sound.play_sound(voice)
            time.sleep(1)

    def split_text(self, text: str) -> list[str]:
        # 。を区切りにしてリストにする
        text = text.replace("\n", "")
        return text.split("。")


if __name__ == "__main__":
    aituber_system = AITuberSystem()
    aituber_system.start()
