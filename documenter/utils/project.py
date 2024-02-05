from dataclasses import dataclass
from typing import List
import logging

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser

from langchain_core.documents import Document


@dataclass
class PreLoader:
    @classmethod
    def load_documents(
            cls,
            root_dir: str, 
            file_types: List[str] = None,
            ignore_paths: List[str] = None
    ) -> List[Document]:
        """
            This method will return a globed list of files in a directory and it's subdirectories. 
                Will exclude hidden files and directories.

            Args:
                root_dir (str): The root directory to search for files.
                file_types (List[str]): The file types to search for. If None, all files will be returned.
                ignore_paths (List[str]): A list of paths to ignore. glob style paths are supported.
            Returns:
                List[str]: A list of file paths.
        """
        loader = GenericLoader.from_filesystem(
            path=root_dir,
            glob="**/*",
            suffixes=cls._check_file_extensions(file_types) if file_types else None,
            exclude=ignore_paths,
            parser=LanguageParser(language=Language.PYTHON)
        )
        return loader.load()

    @staticmethod
    def _check_file_extensions(
            file_types: List[str]) -> List[str]:
        """
            This method will check if the file extensions are formatted correctly.
                If not, it will format them correctly and adds potential documentation file types.
                
            Args:
                file_types (List[str]): The file types to check.
            Returns:
                List[str]: A list of correctly formatted unique file types.
        """
        documentation_file_types = ['.md', '.rst', '.txt']
        for counter, item in enumerate(file_types):
            if not item.startswith('.'):
                file_types[counter] = f'.{item}'
        file_types = list(set(file_types + documentation_file_types))
        logging.info(f"File types: {file_types}")
        return file_types
