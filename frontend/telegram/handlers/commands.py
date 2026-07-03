import httpx
from telegram import Update
from telegram.ext import ContextTypes

from frontend.telegram.keyboards.reply import main_keyboard
from frontend.telegram.settings import bot_settings

API = bot_settings.api_base_url
HEADERS = {"Authorization": f"Bearer {bot_settings.api_key}"} if bot_settings.api_key else {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"Привет, {user.first_name or 'пользователь'}!\n\n"
        "Я бот pod-ft для проверки соответствия требованиям ПОД/ФТ/ФРОМУ.\n\n"
        "Доступные команды:\n"
        "/ask <вопрос> — задать вопрос\n"
        "/stats — статистика по источникам\n"
        "/help — справка\n"
        "/cancel — отменить текущий диалог",
        reply_markup=main_keyboard(),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "pod-ft — платформа RAG для compliance-проверки.\n\n"
        "Как использовать:\n"
        "1. /ask <ваш вопрос> — получите ответ с цитатами из нормативных документов\n"
        "2. /stats — просмотр текущей статистики\n\n"
        "Источники: 115-ФЗ, 262-ФЗ, положения Банка России, ПВК.",
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    from frontend.telegram.handlers.questions import ANSWER

    await update.message.reply_text("Диалог отменён.")
    return ANSWER


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Запрашиваю статистику...")
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(f"{API}/sources", headers=HEADERS, timeout=10)
            if resp.status_code == 200:
                sources = resp.json().get("sources", [])
                text = f"📊 Всего источников: {len(sources)}\n"
                for s in sources[:10]:
                    text += f"  • {s.get('title', s.get('name', '?'))}\n"
                await update.message.reply_text(text)
            else:
                await update.message.reply_text(f"Ошибка: HTTP {resp.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Ошибка соединения: {e}")
