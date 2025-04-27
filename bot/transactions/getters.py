from aiogram_dialog import DialogManager
from bot.user.dao import TransactionsDAO
from datetime import date
from loguru import logger
import datetime


async def get_transactions(dialog_manager: DialogManager, **kwargs):
    data: date = dialog_manager.dialog_data["date"]
    user_id = dialog_manager.dialog_data["user_id"]
    session = dialog_manager.middleware_data.get("session_with_commit")

    transactions = await TransactionsDAO(session).transactions_to_data(data, user_id)

    text = (
        "<b>📅 Вот ваши траты</b>\n\n"
        f"<b>📆 Дата:</b> {data.strftime('%Y-%m-%d')}\n\n\n"
    )

    trans_list = [transaction.to_dict() for transaction in transactions]

    for i, item in enumerate(trans_list):
        text +=(
            f"<b>Покупка №{i}</b>\n"
            f"  категория: <b>{item['cat'].value}</b>\n"
            f"  цена: <b>{item['price']}</b>\n"
            f"  описание: <b>{item['description']}</b>\n\n"
        )

    return {
            "trans_list": text,
        }