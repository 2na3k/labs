import os, json
from enum import Enum
from dotenv import load_dotenv
from dataclasses import dataclass

# list of client i currently using
import google.generativeai as ggai
from groq import Groq
import ollama


# init load the .env file
# todo: should we deal with dotenv here?
load_dotenv()


class ModelName(Enum):
    llama3_2_3b = "llama3_2_3b"
    llama3_1_8b = "llama3_1_8b"
    gemini_pro = "gemini_pro"

    @classmethod
    def to_list(cls) -> list: ...


"""
Client list:
- gemini -> google generative ai one 
- groq -> groq -> llama3_1
- 

Rules: 
- always export all the environment variable to the keys
- system prompt is hackable, and can be changed within the chat
"""


@dataclass
class ResponseModel:
    role: str
    content: str

    @classmethod
    def to_dict(cls):
        return {"role": cls.role, "content": cls.content}


class ModelClientBase:
    def __init__(self, model_name: str):
        """
        what to do in here:
        - init the client, assign that to the self.client
        """
        self.client = None
        self.model = model_name

    def chat(self, *args, **kwargs) -> ResponseModel:
        raise NotImplementedError()


# simple implementation
class GroqClient(ModelClientBase):
    """
    Copied from here: https://console.groq.com/docs/libraries

    TODOS:
    - where to input system prompt -> prevent overriding the system-prompt in the level of something?
    - params -> to each chat
    """

    def __init__(self, model_name):
        self.client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
        self.system_prompt = {
            "role": "system",
            "content": "you are an helpful asssistant",
        }
        self.model = model_name

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


class GeminiClient(ModelClientBase):
    """
    https://github.com/google-gemini/cookbook/blob/main/quickstarts/System_instructions.ipynb
    """

    def __init__(self, model_name):
        ggai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = model_name
        self.system_prompt = (
            "You are a coding expert that specializes in front end interfaces. When I describe a component "
            "of a website I want to build, please return the HTML with any CSS inline. Do not give an "
            "explanation for this code."
        )
        self.client = ggai.GenerativeModel(model_name=model_name)

    def chat(self, message: str, params: dict = {}, system_prompt: str = None):
        if system_prompt is not None:
            self.client = ggai.GenerativeModel(
                model_name=self.model_name, system_instruction=system_prompt
            )
        response = self.client.generate_content(message, **params)
        return ResponseModel(role=self.model, content=json.loads(response.text))


class ClientFactory:
    @staticmethod
    def _get_dict_model_list() -> dict:
        """
        Get the mapping between model name and responsible client
        """

    @classmethod
    def get_client(cls, model_name: str) -> ModelClientBase:
        """
        design principle:
        - each client will have the attribute/metadata whether the model is supported with or not
        - each one is something
        """
        model_dict = cls._get_dict_model_list()
        client = model_dict.get(model_name)

        if client == None:
            raise Exception(f"The model type {model_name} is not supported")
        else:
            return client(model_name=model_name)
