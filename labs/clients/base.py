from abc import ABC, abstractmethod
from dataclasses import dataclass
from pydantic.dataclasses import dataclass


@dataclass
class ResponseModel:
    role: str
    content: str

    @classmethod
    def to_dict(cls):
        """
        Just got this for the simplification of the response
        """
        return {"role": cls.role, "content": cls.content}


class ModelClientBase(ABC):
    def __init__(self, model_name: str):
        """
        what to do in here:
        - init the client, assign that to the self.client
        """
        self.client = None
        self.model_name = model_name
        self._has_meta()
        if model_name not in self.list_model:
            raise Exception(f"The model type '{model_name} 'is not support")

    @abstractmethod
    def chat(self, *args, **kwargs) -> ResponseModel:
        raise NotImplementedError()

    @classmethod
    def _has_meta(cls):
        try:
            cls.list_model
        except AttributeError:
            raise Exception("There is no list of supported model for this client")
