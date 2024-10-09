import os, json
from labs.clients.base import ModelClientBase, ResponseModel
import google.generativeai as ggai
from labs.logger import logger

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
        self.model_name = model_name
        self.client = ggai.GenerativeModel(model_name=model_name)

    def chat(self, message: str, params: dict = {}, system_prompt: str = None):
        if system_prompt is not None:
            self.client = ggai.GenerativeModel(
                model_name=self.model_name, system_instruction=system_prompt
            )
        try:
            response = self.client.generate_content(
                contents=message,
                generation_config={
                    "temperature": params.get("temperature"),
                    "max_output_tokens": params.get("max_output_tokens")
                }
            )
            logger.info(f"response: {response.to_dict()}")

            return ResponseModel(role=self.model_name, content=response.text)
        except Exception as e:
            logger.error(f"Caught an exception: {e}")
            return ResponseModel(role=self.model_name, content="Oops, there are some problem with the prompt")
