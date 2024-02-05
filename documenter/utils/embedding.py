import logging
from dataclasses import dataclass
from typing import Callable
import utils.providers.openai as oai_embedding
import utils.providers.ollama as oll_embedding
import utils.providers.huggingface as hf_embedding
import utils.providers.mistralal as mia_embedding

EMBEDDING_FACTORY = {
    "openai": oai_embedding.get_embedding,
    "ollama": oll_embedding.get_embedding,
    "huggingface": hf_embedding.get_embedding,
    "mistralai": mia_embedding.get_embedding
    }


@dataclass
class Embedding:
    provider: str = None
    model: str = None
    handler: Callable = None

    def __post_init__(self):
        if self.provider not in EMBEDDING_FACTORY:
            logging.error(f"Provider {self.provider} not found in EMBEDDING_FACTORY \n Defaulting to Huggingface")
            self.provider = "huggingface"
        self.handler = EMBEDDING_FACTORY[self.provider](self.model)
        logging.info(f"Embedding provider is {self.provider} with model {self.model}")
