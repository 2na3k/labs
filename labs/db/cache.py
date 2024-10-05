import os
import joblib


class CahceHandler:
    def __init__(self) -> None:
        self.init_cache()

    def init_cache():
        try:
            os.mkdir("data/")
        except:
            pass

    def load_cache():
        try:
            return joblib.load("data/past_chats_list")
        except:
            return {}

    def persist_message(message: dict, filename: str):
        joblib.dump(message, filename)
