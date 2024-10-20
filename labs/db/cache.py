import os
import joblib
import streamlit as st
from labs.logger import logger


class CahceHandler:
    """
    Simple cache-on-file module
    P/s: I don't want to apply pydantic model here
    """
    def __init__(self) -> None:
        self.init_cache()

    @staticmethod
    def init_cache():
        try:
            os.mkdir("data/")
        except:
            pass
    
    @staticmethod
    def load_cache():
        try:
            return joblib.load("data/past_chats_list")
        except:
            return {}

    @staticmethod
    def persist_message(messages: dict, filename: str):
        joblib.dump(messages, filename)
    
    @staticmethod
    def load_messages_from_cache():
        try:
            st.session_state.messages = joblib.load(
                f'data/{st.session_state.chat_id}-st_messages'
            )
            st.session_state.model_history = joblib.load(
                f'data/{st.session_state.chat_id}-model_messages'
            )
            logger.info(f'old cache loaded from chat_id {st.session_state.chat_id}')
        except:
            st.session_state.messages = []
            st.session_state.model_history = []
            print(f'new_cache made with id {st.session_state.chat_id}')