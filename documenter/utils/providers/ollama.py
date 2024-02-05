from langchain_community.embeddings import OllamaEmbeddings

default_model= "llama2:7b"


def get_embedding(model: str ):
    if model is None:
        model = default_model
    return OllamaEmbeddings(model=model)