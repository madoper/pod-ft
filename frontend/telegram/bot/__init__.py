from __future__ import annotations

__anchor__ = "telegram-bot"
# schema-ref: project-schema.yaml#/services/17

import asyncio
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from frontend.telegram.handlers.commands import (
    cancel,
    help_command,
    start,
    stats_command,
)
from frontend.telegram.handlers.questions import (
    ANSWER,
    answer_received,
    ask_question,
    question_received,
)
from frontend.telegram.settings import bot_settings

logger = logging.getLogger(__name__)


def build_application() -> Application:
    app = Application.builder().token(bot_settings.bot_token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("stats", stats_command))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("ask", ask_question)],
        states={
            ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, question_received),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(conv_handler)

    return app


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    logger.info("telegram-bot starting")
    yield
    logger.info("telegram-bot stopped")


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    application = build_application()
    async with lifespan():
        await application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    asyncio.run(main())
