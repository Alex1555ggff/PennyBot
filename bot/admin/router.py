from aiogram import Router, F
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from bot.admin.kbs import main_admin_kb, admin_back_kb
from bot.config import settings
from bot.user.dao import UserDAO

router = Router()

@router.callback_query(F.data == "admin_panel", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_start(call: CallbackQuery):
    """
    Обработчик входа в админ-панель. Доступ разрешен только администраторам.
    """
    await call.answer("Доступ в админ-панель разрешен!")
    await call.message.edit_text("Выберите действие:", reply_markup=main_admin_kb())

@router.callback_query(F.data == "admin_users_stats", F.from_user.id.in_(settings.ADMIN_IDS))
async def admin_users_stats(call: CallbackQuery, session_without_commit: AsyncSession):
    """
    Обработчик запроса статистики пользователей.
    Получает общее количество пользователей в базе данных и отправляет информацию админу.
    """
    await call.answer("Загружаю статистику пользователей...")
    users_stats = await UserDAO(session_without_commit).count()
    await call.message.edit_text(f'Всего в базе данных {users_stats} пользователей.', reply_markup=admin_back_kb())