# Client design principles

There might be some design principles for the client:
- For using the client, put only the model name to the `ClientFactory.get_client()`. This would be simplified for model choosing overall.
- System prompt, user customized prompts and params are passed to the chat function of the `ModelClientBase.chat()` for the hacking process (normally, other client would not let us to put those directly from their client).
- For the structure of the `ModelClientBase` interface, the instance of the interface must have the `list_model` as the attribute.