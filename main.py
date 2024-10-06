import time
import streamlit as st

from labs.clients.factory import ClientFactory, get_list_of_available_model
from labs.db.cache import CahceHandler

# well for some reason I can import now
all_model = get_list_of_available_model()
new_chat_id = f'{time.time()}'
AI_AVATAR_ICON = '✨'

class App:
    def __init__(self):
        self.cache = CahceHandler()
        self.past_chats = self.cache.load_cache()

    
    def load_sidebar(self):
        # Sidebar allows a list of past chats
        with st.sidebar:
            st.write("# Model type")
            st.session_state.model_name = st.selectbox(
                key="123",
                options=all_model,
                label='Pick a model',
                placeholder=all_model[0]
            )

            st.session_state.model = ClientFactory.get_client(
                model_name=st.session_state.model_name
            )

            st.write('# Past Chats')
            if st.session_state.get('chat_id') is None:
                st.session_state.chat_id = st.selectbox(
                    key="345",
                    label='Pick a past chat',
                    options=[new_chat_id] + list(self.past_chats.keys()),
                    format_func=lambda x: self.past_chats.get(x, 'New Chat'),
                    placeholder='_',
                )
            else:
                # This will happen the first time AI response comes in
                st.session_state.chat_id = st.selectbox(
                    key="345",
                    label='Pick a past chat',
                    options=[new_chat_id, st.session_state.chat_id] + list(self.past_chats.keys()),
                    index=1,
                    format_func=lambda x: self.past_chats.get(x, 'New Chat' if x != st.session_state.chat_id else st.session_state.chat_title),
                    placeholder='_',
                )
            st.session_state.chat_title = f'ChatSession-{st.session_state.chat_id}'
            

    def load_history(self):
        self.cache.load_messages_from_cache()
        
    
    def load_messages(self):
        for message in st.session_state.messages:
            with st.chat_message(
                name=message['role'],
                avatar=message.get('avatar'),
            ):
                st.markdown(message['content'])
    
    def handle_chat(self):
        if prompt := st.chat_input('Your message here...'):
            if st.session_state.chat_id not in self.past_chats.keys():
                self.past_chats[st.session_state.chat_id] = st.session_state.chat_title
                self.cache.persist_message(self.past_chats, 'data/past_chats_list')
            # Display user message in chat message container
            with st.chat_message('user'):
                st.markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append(
                dict(
                    role='user',
                    content=prompt,
                )
            )
            ## Send message to AI
            response = st.session_state.model.chat(message=prompt)
            with st.chat_message(
                name=st.session_state.model_name,
                avatar=AI_AVATAR_ICON,
            ):
                message_placeholder = st.empty()
                message_placeholder.write(response.content)
            st.session_state.messages.append(
                dict(
                    role=st.session_state.model_name,
                    content=prompt,
                    avatar=AI_AVATAR_ICON,
                )
            )
            st.session_state.model_history.append(
                dict(
                    role=st.session_state.model_name,
                    content=response.content,
                    avatar=AI_AVATAR_ICON,
                )
            )
            self.cache.persist_message(
                st.session_state.messages,
                f'data/{st.session_state.chat_id}-st_messages',
            )
            self.cache.persist_message(
                st.session_state.model_history,
                f'data/{st.session_state.chat_id}-gemini_messages',
            )

    def run(self):
        self.load_sidebar()
        self.load_history()
        self.load_messages()
        self.handle_chat()

if __name__ == "__main__":
    app = App()
    app.run()