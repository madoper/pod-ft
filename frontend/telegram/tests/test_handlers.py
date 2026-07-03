import pytest
from conftest import make_context, make_update

from frontend.telegram.handlers.commands import help_command, start
from frontend.telegram.handlers.questions import ANSWER, ask_question


@pytest.mark.asyncio
async def test_start_handler():
    update = make_update("/start")
    context = make_context()
    await start(update, context)
    assert update.message.replied_text is not None
    assert "pod-ft" in update.message.replied_text


@pytest.mark.asyncio
async def test_help_handler():
    update = make_update("/help")
    context = make_context()
    await help_command(update, context)
    assert update.message.replied_text is not None


@pytest.mark.asyncio
async def test_ask_question_with_text():
    update = make_update("/ask какие сроки?")
    context = make_context()
    result = await ask_question(update, context)
    assert result == ANSWER


@pytest.mark.asyncio
async def test_ask_question_no_text():
    update = make_update("/ask")
    context = make_context()
    result = await ask_question(update, context)
    assert result == ANSWER
