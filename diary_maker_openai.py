from daily_things_maker import DailyThingsMaker
from openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter()

with open("storage/diary_maker_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

daily_things = DailyThingsMaker.make()

user_prompt = daily_things
res = adapter.chat_completions([adapter.create_message(
    "system", system_prompt), adapter.create_message("user", user_prompt)])
print(f"出来事：{daily_things}")
print(f"日記：{res}")
