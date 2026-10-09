from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class PromptArgumentDefinition:
    name: str
    description: str
    required: bool = True


@dataclass(frozen=True)
class PromptDefinition:
    name: str
    description: str
    arguments: list[PromptArgumentDefinition]
    handler: Callable[..., str]
