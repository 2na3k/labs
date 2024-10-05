from dotenv import load_dotenv
from labs.clients.base import ModelClientBase
from inspect import isclass

load_dotenv()


def get_list_client_object() -> list:
    import importlib

    modules = importlib.import_module("labs.clients.impl")

    return [
        getattr(modules, mod)
        for mod in modules.__dir__()
        if isclass(getattr(modules, mod))
        and not mod.startswith("__")
        and issubclass(getattr(modules, mod), ModelClientBase)
        and mod != "ModelClientBase"
    ]


def get_list_of_available_model() -> list:
    list_object = get_list_client_object()
    return [model for client in list_object for model in client.list_model]


class ClientFactory:
    @staticmethod
    def _get_dict_model_list() -> dict:
        """
        Get the mapping between model name and responsible client
        """
        list_object = get_list_client_object()
        return {model: client for client in list_object for model in client.list_model}

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
