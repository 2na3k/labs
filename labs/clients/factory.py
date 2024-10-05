from dotenv import load_dotenv
from labs.clients.base import ModelClientBase

load_dotenv()


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


def get_list_of_available_model() -> list:
    import importlib

    print(importlib.import_module("labs.clients.impl"))