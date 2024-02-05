from langchain_mistralai import MistralAIEmbeddings
from httpcore import LocalProtocolError
import logging
from os import getenv

default_model = "mistral-embed"
default_mistral_api_key = getenv("MISTRAL_API_KEY")


def get_embedding(model: str):
    if model is None:
        model = default_model
    try:
        mistral_embedding = MistralAIEmbeddings(
            model=model,
            mistral_api_key=default_mistral_api_key)
    except LocalProtocolError as e:
        # this is added to catch the LocalProtocolError that is raised when the mistralai server telling you
        # that you do not have a subscription active (at least that is what I think it is supposed to do 429 error code)
        logging.error(f"LocalProtocolError: {e}")
        return None

    return mistral_embedding
