import os, json
from labs.clients.base import ModelClientBase, ResponseModel
import google.generativeai as ggai


class GeminiClient(ModelClientBase):
    """
    https://github.com/google-gemini/cookbook/blob/main/quickstarts/System_instructions.ipynb
    """

    list_model = [
        "gemini-1.5-flash",
        "gemini-1.5-flash-002"
    ]

    def __init__(self, model_name):
        super().__init__(model_name)
        ggai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.system_prompt = (
            "You are a helpful assistant."
        )
        self.client = ggai.GenerativeModel(model_name=model_name)

    def chat(self, message: str, params: dict = {}, system_prompt: str = None):
        if system_prompt is not None:
            self.client = ggai.GenerativeModel(
                model_name=self.model_name, system_instruction=system_prompt
            )
        response = self.client.generate_content(message, **params)

        return ResponseModel(role=self.model, content=response.text)
