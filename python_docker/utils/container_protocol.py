from dataclasses import dataclass
from typing import Protocol, Dict, runtime_checkable


@dataclass
@runtime_checkable
class Container(Protocol):
    image: str
    timeout: str
    image_selection_dict: Dict[str, str]

    def _determine_image(self) -> str:
        raise NotImplementedError

    def create(self, name: str = None, timeout: str = None):
        raise NotImplementedError

    def start(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def command(self, command: str) -> str:
        raise NotImplementedError
