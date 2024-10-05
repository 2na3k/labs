from labs.clients.factory import *
from labs.clients.impl.gemini import GeminiClient


def test_get_list_of_available_model():
    list_models = get_list_of_available_model()


def test_client_factory():
    client = ClientFactory.get_client(model_name="gemini-1.5-flash-002")
    assert isinstance(client, GeminiClient)
