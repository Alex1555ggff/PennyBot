from datetime import date
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
from bot.user.schemas import STransactions, SUser
from bot.user.kbs import main_user_kb
from bot.user.dao import UserDAO, TransactionsDAO
from bot.dao.models import CatEnum
from bot.user.state import AddTransactionsState
from bot.config import broker


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий отменен!")
    await callback.message.answer("Вы отменили сценарий добавления записи.",
                                  reply_markup=main_user_kb(callback.from_user.id))
    

async def category_selected(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    cat = str(button.widget_id)
    dialog_manager.dialog_data["cat"] = cat
    await callback.answer(f"Выбрана категория {cat}")
    await dialog_manager.switch_to(AddTransactionsState.price)


async def on_confirm(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    session = dialog_manager.middleware_data.get("session_with_commit")

    cat = CatEnum(dialog_manager.dialog_data["cat"])
    description = dialog_manager.find("description").get_value()
    price = dialog_manager.find("price").get_value()
    user_id = callback.from_user.id

    await callback.answer("Приступаю к сохранению")

    try:
        transactions_data = STransactions(
            cat=cat,
            description=description,
            price=price, 
            user_id=user_id
        )
    except:
        await callback.answer("Ошибка при добавлении записи\n" \
                                "Некоторые данные не валидны")
        await dialog_manager.back()

    transactions = await TransactionsDAO(session).create_transactions(transactions_data)

    if transactions is None:
        await callback.answer("Ошибка при добавлении записи")
        await dialog_manager.back()

    await callback.answer(f"Запись успешно создана!")
    text = "Запись успешно создана! Со списком своих трат можно ознакомиться в меню 'Мои Расходы'"
    await callback.message.answer(text, reply_markup=main_user_kb(user_id))

    admin_text = (
            f"Внимание! Пользователь с ID {callback.from_user.id} добавил запись!\n"
            f"Username: {callback.from_user.username}\n"
            f"Transactions: {transactions.cat}"
        )

    await broker.publish(admin_text, "admin_msg")
    await broker.publish(callback.from_user.id, "noti_user")
    await dialog_manager.done()
    
        
