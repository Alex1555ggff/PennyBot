from aiogram_dialog import DialogManager
from bot.user.dao import  TransactionsDAO
from datetime import date
from loguru import logger
import datetime


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    """Получение данных для подтверждения."""
    cat = dialog_manager.dialog_data["cat"]
    description = dialog_manager.find("description").get_value()
    price = dialog_manager.find("price").get_value()

    confirmed_text = (
        "<b>📅 Подтверждение записи</b>\n\n"
        f"<b>📆 Дата:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"<b>Информация о траты:</b>\n"
        f"  - 📝 Описание: {description}\n"
        f"  - 👥 Категория: {cat}\n"
        f"  - 📍 Цена: {price}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}


async def get_transactions(dialog_manager: DialogManager, **kwargs):
    data: date = dialog_manager.dialog_data["date"]
    user_id = dialog_manager.dialog_data["user_id"]
    session = dialog_manager.middleware_data.get("session_with_commit")

    transactions = await TransactionsDAO(session).transactions_to_data(data, user_id)

    trans_list = [transaction.to_dict() for transaction in transactions]

    return {
            "trans_list": trans_list,
        }