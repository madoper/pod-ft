"""Test fixtures for Telegram bot tests."""

from dataclasses import dataclass, field
from typing import Any

import pytest


@dataclass
class FakeMessage:
    text: str | None
    replied_text: str | None = None
    edited_text: str | None = None

    async def reply_text(self, text: str, **kwargs: Any) -> "FakeMessage":
        self.replied_text = text
        return self

    async def edit_text(self, text: str, **kwargs: Any) -> None:
        self.edited_text = text


@dataclass
class FakeUser:
    first_name: str = "TestUser"
    id: int = 12345
    is_bot: bool = False


@dataclass
class FakeUpdate:
    message: FakeMessage
    effective_user: FakeUser = field(default_factory=FakeUser)

    @property
    def effective_message(self):
        return self.message


@dataclass
class FakeContext:
    user_data: dict = field(default_factory=dict)
    bot_data: dict = field(default_factory=dict)


def make_update(text: str | None) -> FakeUpdate:
    return FakeUpdate(message=FakeMessage(text=text))


def make_context() -> FakeContext:
    return FakeContext()


@pytest.fixture
def update():
    return make_update


@pytest.fixture
def context():
    return make_context
