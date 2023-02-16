from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Note(_message.Message):
    __slots__ = ["length", "message", "recipient", "sender"]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_FIELD_NUMBER: _ClassVar[int]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    length: int
    message: str
    recipient: str
    sender: str
    def __init__(self, sender: _Optional[str] = ..., recipient: _Optional[str] = ..., length: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...

class Text(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...
