from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove


def main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            ["/ask Задать вопрос", "/stats Статистика"],
            ["/help Помощь"],
        ],
        resize_keyboard=True,
    )


def cancel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [["/cancel Отмена"]],
        resize_keyboard=True,
    )


def remove_keyboard() -> ReplyKeyboardRemove:
    return ReplyKeyboardRemove()
