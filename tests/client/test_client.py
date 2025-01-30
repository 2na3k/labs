from labs.clients.impl.gemini import GeminiClient
from labs.clients.impl.groq import GroqClient
from labs.clients.impl.openai import OpenAIClient

def test_groq_client():
    """
    Should use fixure
    """
    client = GroqClient(model_name="llama-3.1-8b-instant")
    response = client.chat(message="hello?")


def test_gemini_client():
    client = GeminiClient(model_name="gemini-1.5-flash")
    response = client.chat(message="hello?")
    assert response.content != None


def test_openai_client():
    client = OpenAIClient(model_name="deepseek-r1:14b")
    response = client.chat(message="hello?")
    assert response.content != None
