from openai_adapter import OpenAIAdapter

adapter = OpenAIAdapter()

with open("storage/diary_maker_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# ここをあとで一日生成機で作成する
user_prompt = """
家→学校：目覚ましを入れ忘れて寝坊した
学校：友達が昼休みにコケて弁当を床に落とした
学校→予備校：喫茶店で新作のコーヒーを飲んだ
予備校：小テストで名前を書き忘れて怒られた
予備校→家：コンビニでコッソリ買った肉まんが凄い美味しかった
家：窓をみたら星空がきれいに見えた
"""

res = adapter.chat_completions([adapter.create_message(
    "system", system_prompt), adapter.create_message("user", user_prompt)])

print(res)
