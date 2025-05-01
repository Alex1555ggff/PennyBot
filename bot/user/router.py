from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher.router import Router
from aiogram_dialog import DialogManager, StartMode
from pydantic import create_model
from sqlalchemy.ext.asyncio import AsyncSession
from bot.user.state import AddTransactionsState
from bot.transactions.state import GetTransactionsState
from bot.user.kbs import main_user_kb
from bot.user.schemas import SUser
from bot.user.dao import UserDAO, TransactionsDAO
from loguru import logger


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session_with_commit: AsyncSession, state: FSMContext):
    await state.clear()
    user_data = message.from_user
    user_id = user_data.id
    user_info = await UserDAO(session_with_commit).find_one_or_none_by_id(user_id)
    if user_info is None:
        user_schema = SUser(id=user_id, first_name=user_data.first_name,
                            last_name=user_data.last_name, username=user_data.username)
        await UserDAO(session_with_commit).create_user(user_schema)
    text = ("👋 Добро пожаловать!\n"
            "Тут ты можешь следить за своими расходами")
    await message.answer(text, reply_markup=main_user_kb(user_id))


@router.callback_query(F.data == "create_trn")
async def create_transactions(call: CallbackQuery, dialog_manager: DialogManager):
    await call.answer('Добавление записи')
    await dialog_manager.start(state=AddTransactionsState.category, mode=StartMode.RESET_STACK)


@router.callback_query(F.data == "check_trn")
async def check_transactions(call: CallbackQuery, dialog_manager: DialogManager):
    await call.answer('Просмотр трат')
    await dialog_manager.start(state=GetTransactionsState.select_method, mode=StartMode.RESET_STACK)


@router.callback_query(F.data == "delete_trn")
async def delete_transactions(call: CallbackQuery, dialog_manager: DialogManager):
    await call.answer('Добавление записи')
    await dialog_manager.start(state=AddTransactionsState.category, mode=StartMode.RESET_STACK)