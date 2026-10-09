from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ResourceDefinition:
    uri: str
    name: str
    description: str
    mime_type: str | None
    read: Callable[[], str]
