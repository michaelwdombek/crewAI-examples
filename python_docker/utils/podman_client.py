# https://pypi.org/project/podman/
from podman import PodmanClient
from dataclasses import dataclass, field
from typing import List
from uuid import uuid4
import logging


@dataclass
class Container:
    timeout: str = "infinity"       # timeout in seconds
    image: str = None               # image to use
    container: PodmanClient.containers = field(init=False, default=None, repr=False)
    client: PodmanClient = field(init=False, default=None, repr=False)
    image_selection_dict = {
        "darwin": "python:3.12-alpine",                          # default for mac
        "linux": "python:3.12-alpine",                          # default for linux
        "win32": "python:3.12-windowsservercore-ltsc2022",      # default for windows
        "other": "python:3.12-ubuntu"                           # default for other
    }

    def __post_init__(self):
        self.container = PodmanClient(base_url="unix:///run/user/1000/podman/podman.sock")

    def _determine_image(self) -> str:
        raise NotImplementedError

    def create(self, name: str = None, command: str | List[str] = None):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def command(self, command: str) -> str:
        raise NotImplementedError