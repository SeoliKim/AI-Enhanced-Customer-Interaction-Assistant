from dataclasses import dataclass, field
from typing import Literal
from enum import Enum

import mesop as me

Role = Literal["user", "model"]

@dataclass(kw_only=True)
class ChatMessage:
    role: Role = "user"
    content: str = ""
    in_progress: bool = False

@dataclass
class Conversation:
    model: str = ""
    messages: list[ChatMessage] = field(default_factory=list)

@me.stateclass
class State:
    input: str = ""
    conversations: list[Conversation] = field(default_factory=list)

@me.stateclass
class ModelDialogState:
    model: list[str] = field(default_factory=list)