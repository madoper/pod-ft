import httpx
from telegram import Update
from telegram.ext import ContextTypes

from frontend.telegram.keyboards.reply import cancel_keyboard
from frontend.telegram.settings import bot_settings

ANSWER = range(1)

API = bot_settings.api_base_url
HEADERS = {"Authorization": f"Bearer {bot_settings.api_key}"} if bot_settings.api_key else {}


async def ask_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    text = update.message.text
    question = text.removeprefix("/ask").strip() if text else ""

    if question:
        context.user_data["pending_question"] = question
        await process_question(update, context)
        return ANSWER

    await update.message.reply_text(
        "Введите ваш вопрос по ПОД/ФТ/ФРОМУ:",
        reply_markup=cancel_keyboard(),
    )
    return ANSWER


async def question_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    question = update.message.text.strip()
    if not question:
        await update.message.reply_text("Пожалуйста, введите вопрос.")
        return ANSWER

    context.user_data["pending_question"] = question
    return await process_question(update, context)


async def process_question(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    question = context.user_data.get("pending_question", "")

    if len(question) > bot_settings.max_question_length:
        await update.message.reply_text(
            f"Вопрос слишком длинный (макс. {bot_settings.max_question_length} символов)."
        )
        return ANSWER

    msg = await update.message.reply_text("🔍 Ищу ответ...")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{API}/answer",
                json={"question": question, "channel": "telegram"},
                headers=HEADERS,
                timeout=15,
            )

            if resp.status_code == 200:
                data = resp.json()
                answer_data = data.get("answer") or {}
                summary = answer_data.get("summary", "Ответ не получен.")
                llm_summary = answer_data.get("llm_summary")
                citations = answer_data.get("citations", [])

                text = ""
                if llm_summary:
                    text += f"💡 *Краткое изложение:*\n{llm_summary}\n\n"
                text += f"*Ответ:*\n{summary}\n\n"
                if citations:
                    text += "*Источники:*\n"
                    for i, c in enumerate(citations[:5], 1):
                        label = c.get("citation_label", f"Фрагмент {i}")
                        snippet = c.get("quote", "")[:150]
                        text += f"  {i}. {label}: {snippet}...\n"
                else:
                    text += "_Нет цитируемых источников._"

                await msg.edit_text(text, parse_mode="Markdown")
            else:
                await msg.edit_text(f"Ошибка сервера: HTTP {resp.status_code}")
    except Exception as e:
        await msg.edit_text(f"Ошибка: {e}")

    return ANSWER
