from datetime import date
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from bot.user.schemas import SExpenses, STransactions, SUser
from bot.user.kbs import main_user_kb
from bot.user.dao import UserDAO, TransactionsDAO
from bot.transactions.state import GetTransactionsState


async def cancel_logic(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await callback.answer("Сценарий бронирования отменен!")
    await callback.message.answer("Вы отменили сценарий бронирования.",
                                  reply_markup=main_user_kb(callback.from_user.id))
    

async def process_date_selected(callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date):
    """Обработчик выбора даты."""
    dialog_manager.dialog_data["date"] = selected_date
    dialog_manager.dialog_data["user_id"] = callback.from_user.id
    await dialog_manager.switch_to(GetTransactionsState.transactions)