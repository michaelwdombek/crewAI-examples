#from langchain_community.embeddings import HuggingFaceEmbeddings
import logging

from langchain_community.embeddings import HuggingFaceHubEmbeddings

def get_embedding(model: str = "sentence-transformers/all-MiniLM-l6-v2"):
    logging.info(f"Using HuggingFace model: {model}")
    return HuggingFaceHubEmbeddings(model=model)

