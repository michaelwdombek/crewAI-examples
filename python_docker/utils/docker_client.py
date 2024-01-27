from dataclasses import dataclass, field
from docker import client as docker
from uuid import uuid4
import logging
from sys import platform


@dataclass
class Container:
    """
    Wrapper class for docker containers

    Args:
        timeout (str, optional): timeout in seconds. Defaults to "infinity".
        image (str, optional): image to use. Defaults to None.
        container (docker.DockerClient.containers, optional): container object. Defaults to None.
        client (docker.DockerClient, optional): docker client. Defaults to None.
        image_selection_dict (dict, optional): dictionary containing the image selection. Defaults to None.

    """
    timeout: str = field(default="infinity")       # timeout in seconds
    image: str = None               # image to use
    container: docker.DockerClient.containers = field(init=False, default=None, repr=False)
    client: docker.DockerClient = field(init=False, default=None, repr=False)
    image_selection_dict = {
        "darwin": "python:3.12-alpine",                          # default for mac
        "linux": "python:3.12-alpine",                          # default for linux
        "win32": "python:3.12-windowsservercore-ltsc2022",      # default for windows
        "other": "python:3.12-ubuntu"                           # default for other
    }

    def __post_init__(self):
        self.client = docker.DockerClient.from_env()

    def _determine_image(self) -> str:
        """
        Determines which image to use, if plattform is
            - windows use windowsservercore-ltsc2022
            - linux use alpine
            - mac use alpine

        Returns:
            image (str): image to use
        """
        try:
            return self.image_selection_dict[platform]
        except KeyError:
            logging.warning(f"Platform {platform} is not supported, using default image, {self.image_selection_dict['other']}")
            return self.image_selection_dict["other"]

    def create(self, name: str = None, timeout: str = None):
        """
        creates a container with the given name
        Args:
            name (str, optional): name of the container. Defaults will fall back to uuid4 str.
            timeout (str, optional): timeout in seconds. Defaults to "infinity".
        """

        self.container = self.client.containers.create(
            image=self.image if self.image is not None else self._determine_image(),
            command=f"sleep {self.timeout if timeout is None else timeout}",
            name=name if name else str(uuid4())
            )
        logging.info(f'created container {self.container.name}')


    def start(self):
        """
        starts the container
        Returns:

        """
        self.container.start()
        logging.info(f'started container {self.container.name}, {self.container.logs()}')

    def command(self, command: str) -> str:
        """
        executes a command in the container

        Args:
            command (str): command to execute

        Returns:
            str: output of the command
        """
        return self.container.exec_run(command).output.decode('utf-8')

    def stop(self):
        """
        stops the container
        Returns:

        """
        logging.info(f'stopping container {self.container.name}')
        self.container.stop()

    def remove(self):
        """
        removes the container

        """
        self.container.remove()
        logging.info(f'removed container {self.container.name}')
