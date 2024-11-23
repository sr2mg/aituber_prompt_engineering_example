import random
from pydantic import BaseModel
from openai_adapter import OpenAIAdapter


class Event(BaseModel):
    file_name: str
    place: str
    thing: str


class DailyEventMaker:
    def make() -> str:
        events = DailyEventMaker.__load_random_events()
        events_str = "\n".join(
            [f"{event.place}:{event.thing}" for event in events])

        with open("storage/daily_things_make_prompt.txt", "r", encoding="utf-8") as f:
            system_prompt = f.read()

        adapter = OpenAIAdapter()
        res = adapter.chat_completions([adapter.create_message(
            "system", system_prompt), adapter.create_message("user", events_str)])
        return res

    def __load_random_events() -> list[Event]:
        event_list = [
            {"file_name": "home_to_school", "place": "家→学校"},
            {"file_name": "school", "place": "学校"},
            {"file_name": "school_to_cram_school", "place": "学校→予備校"},
            {"file_name": "cram_school", "place": "予備校"},
            {"file_name": "cram_school_to_home", "place": "予備校→家"},
            {"file_name": "home", "place": "家"},
        ]
        events = []
        for event in event_list:
            with open(f"storage/daily_things_words/{event['file_name']}.txt", "r", encoding="utf-8") as f:
                random_event = random.choice(f.read().splitlines())
                events.append(
                    Event(file_name=event["file_name"], place=event["place"], thing=random_event))
        return events


if __name__ == "__main__":
    print(DailyEventMaker.make())
