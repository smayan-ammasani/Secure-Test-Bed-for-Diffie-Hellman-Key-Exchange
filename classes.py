"""Serializable message classes used by the chat clients."""

from dataclasses import dataclass


@dataclass(slots=True)
class DHInit:
    p: int
    g: int
    public: int


@dataclass(slots=True)
class DHResp:
    public: int


@dataclass(slots=True)
class SecureMessage:
    ciphertext: str


@dataclass(slots=True)
class Message:
    text: str
