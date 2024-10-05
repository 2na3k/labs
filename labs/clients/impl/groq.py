import os
from labs.clients.base import ModelClientBase, ResponseModel
from groq import Groq


class GroqClient(ModelClientBase):
    """
    Copied from here: https://console.groq.com/docs/libraries
    """

    list_model = [
        "llama-3.1-70b-versatile",
        "llama-3.1-8b-instant",
        "llama-3.2-1b-preview",
        "llama3-8b-8192",
    ]

    def __init__(self, model_name):
        super().__init__(model_name)
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.system_prompt = {
            "role": "system",
            "content": "you are an helpful asssistant",
        }

    def chat(
        self, message: str, params: dict = {}, system_prompt: dict = None
    ) -> ResponseModel:
        """
        Response schema (dict):
        - role: str
        - content: str
        """
        system_prompt = (
            system_prompt if system_prompt is not None else self.system_prompt
        )
        response = self.client.chat.completions.create(
            messages=[system_prompt, {"role": "user", "content": message}],
            model=self.model,
            **params,
        ).to_dict()

        return ResponseModel(
            role=response["choices"][0]["message"]["role"],
            content=response["choices"][0]["message"]["content"],
        )
