"""Telegram bot entry point."""
import asyncio

from frontend.telegram.bot import main

if __name__ == "__main__":
    asyncio.run(main())
