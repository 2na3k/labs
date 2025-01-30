import os
from labs.clients.base import ModelClientBase, ResponseModel
from openai import OpenAI

DEFAULT_ENDPOINT = "http://localhost:11434/v1" if os.environ.get("OPENAI_API_KEY") is None else None
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") if os.environ.get("OPENAI_API_KEY") is not None else "ollama"


class OpenAIClient(ModelClientBase):
    """
    Fuck OpenAI
    """

    list_model = [
        "deepseek-r1:14b",
        "qwen2.5-coder:14b"
    ]
    
    def __init__(self, model_name):
        self.client = OpenAI(
            base_url = DEFAULT_ENDPOINT,
            api_key=OPENAI_API_KEY, # required, but unused
        )
        self.system_prompt = None
        self.model_name = model_name

    def chat(
        self, message: str, params: dict = {}, system_prompt: str = None
    ) -> ResponseModel:
        """
        Chat param shape:
        {
            "max_tokens": st.session_state.max_token,
            "top_p": st.session_state.top_p,
            "temperature": st.session_state.temperature,
            "frequency_penalty": st.session_state.frequency_penalty,
            "presence_penalty": st.session_state.presence_penalty
        }
        """ 
        system_prompt = {
            "role": "system",
            "content": system_prompt if system_prompt is not None else self.system_prompt
        }
            
        response = self.client.chat.completions.create(
            messages=[system_prompt, {"role": "user", "content": message}],
            model=self.model_name,
            **params,
        ).to_dict()

        return ResponseModel(
            role=response["choices"][0]["message"]["role"],
            content=response["choices"][0]["message"]["content"],
        )