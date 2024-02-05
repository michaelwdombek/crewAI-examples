import logging
import os
from uuid import uuid5, NAMESPACE_DNS
from dataclasses import dataclass, field
import chromadb as chroma_native


@dataclass
class Session:
    """
        This class will create a session directory and a chromadb for the session.

        Args:
            repo_dir (str): The directory to create a session for.
            base_dir (str): The base directory to create the session in.
            dir (str): The session directory.
            id (str): The session id.
            db (ChromaDB): The chromadb for the session.
    """
    repo_dir: str
    base_dir: str = "./work_dir"
    persistence: bool = False
    dir: str = field(init=False, default=None)
    id: str = field(init=False, default=None)
    db: chroma_native.Client = field(init=False, default=None, repr=False)

    def __post_init__(self) -> None:
        self._generate_session_from_directory()
        if self.persistence:
            self._persistent_session()
        else:
            self._session_db()

    def _generate_session_from_directory(self) -> None:
        """
            This method will generate a stable UUID for a directory based on the lookup directory.

        Returns:

        """
        # Normalize the path by expanding the user directory and resolving to an absolute path
        normalized_path = os.path.abspath(os.path.expanduser(self.repo_dir))
        stable_uuid = uuid5(NAMESPACE_DNS, normalized_path)
        self.id = str(stable_uuid)
        self.dir = f"{self.base_dir}/{self.id}"
        logging.info(f"Session directory is {self.dir}, with id {self.id}")

    def _session_db(self) -> None:
        """
            This method create a chromadb in the session directory if persistence was set, else builds an in mem chromadb.
        Returns:
        """

        db_path = f"{self.dir}/chromadb"
        if self.persistence:
            logging.info(f"loading/creating chromadb at {db_path}")
            chroma_native_session = chroma_native.PersistentClient(path=db_path)
        else:
            logging.info(f"creating in memory chromadb")
            chroma_native_session = chroma_native.Client()
        chroma_native_session.get_or_create_collection(name=self.id)
        self.db = chroma_native_session

    @staticmethod
    def _setup_dir(directory: str) -> None:
        """
            This method will create the directory if it does not exist.

            Args:
                directory (str): The directory to create.
        Returns:
        """
        if not os.path.exists(directory):
            os.mkdir(directory)

    def _persistent_session(self) -> None:
        """
            This method will create a persistent chromadb for the session amd the necessary file structure.
        Returns:
        """
        logging.info(f"Creating persistent session at {self.dir}")
        # we ensure that base and session directory exists
        self._setup_dir(directory=self.base_dir)
        self._setup_dir(directory=self.dir)

        # load or create the vector db
        self._session_db()
