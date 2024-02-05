import logging

from langchain_openai import OpenAIEmbeddings

default_model = "text-embedding-3-large"


def get_embedding(model: str):
    if model is None:
        model = default_model
    logging.info(f"Loading OpenAI model {model} as Embedding provider")
    return OpenAIEmbeddings(model=model)
