from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.config import settings


def main_user_kb(user_id: int) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()

    kb.add(InlineKeyboardButton(text="Добавить запись", callback_data="create_trn"))
    kb.add(InlineKeyboardButton(text="Просмотреть записи", callback_data="check_trn"))
    kb.add(InlineKeyboardButton(text="Удаление записи", callback_data="delete_trn"))
    kb.add(InlineKeyboardButton(text="ℹ️ О нас", callback_data="about_us"))

    if user_id in settings.ADMIN_IDS:
        kb.add(InlineKeyboardButton(text="🔐 Админ-панель", callback_data="admin_panel"))

    kb.adjust(1)
    return kb.as_markup()
