from dataclasses import dataclass
from langchain_community.vectorstores import Chroma
import logging


@dataclass
class Loader:
    @staticmethod
    def update(documents, client: Chroma) -> None:
        """
        This method will update the chroma db collection with the documents.
        Args:
            documents: List of documents to update the collection with.
            client: LC Chroma Client used to connect to ChromaDB

        Returns:

        """
        client.add_documents(documents=documents)
        logging.info(f"Documents successfully added to collection")
# TODO:
# We should add a flow to lookup if the doc is already in the collection and only add if it's not.
# currently it will add the same doc multiple times if the update is run multiple time