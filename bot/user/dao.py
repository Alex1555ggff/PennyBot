from datetime import date, datetime
from zoneinfo import ZoneInfo
from typing import Dict
from loguru import logger
from sqlalchemy import select, update, delete, func, and_
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from bot.dao.base import BaseDAO
from bot.dao.models import User, Transactions, CatEnum

from bot.user.schemas import SUser, STransactions, SExpenses


moscow_tz = ZoneInfo("Europe/Moscow")


class UserDAO(BaseDAO[User]):

    model = User

    async def create_user(self, user_data: SUser):
        try:
            user_data_dict = user_data.model_dump(exclude_unset=True)
            new_user = User(**user_data_dict)

            if self._session is None or not self._session.is_active:
                raise RuntimeError("Сессия неактивна или закрыта!")
            
            self._session.add(new_user)
            logger.info(f"добавлен пользователь {user_data}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании пользователя {e}")
            raise


class TransactionsDAO(BaseDAO[Transactions]):

    model = Transactions

    async def create_transactions(self, trans_data: STransactions):
        try:
            trans_data_dict = trans_data.model_dump()
            new_transaction = Transactions(**trans_data_dict)
            self._session.add(new_transaction)
            logger.info(f"Пользователь {trans_data.user_id} успешно добавил транзакцию {trans_data.cat.value}")
            return new_transaction
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при создании транзакции {e}")
            raise


    async def transactions_to_timedelta(self, start_date: date, end_date: date, user_id: int) -> list[Transactions]:
        try:

            start_datetime = datetime.combine(start_date, datetime.min.time())
            end_datetime = datetime.combine(end_date, datetime.max.time()) 

            query = (select(self.model)
                     .where(and_(
                         self.model.created_at >= start_datetime,
                         self.model.created_at <= end_datetime,
                         self.model.user_id <= user_id,
                     )))
            results = await self._session.execute(query)
            return results.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении транзакций {e}, по дате")
    

    async def transactions_to_data(self, selected_data: date, user_id: int) -> list[Transactions]:
        try:

            start_datetime = datetime.combine(selected_data, datetime.min.time())
            end_datetime = datetime.combine(selected_data, datetime.max.time()) 

            query = (select(self.model)
                     .where(and_(
                         self.model.created_at >= start_datetime,
                         self.model.created_at <= end_datetime,
                         self.model.user_id <= user_id,
                     )))
            results = await self._session.execute(query)
            return results.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при получении транзакций {e}, по дате")

    
    @classmethod
    async def expenses_to_timedelta(trans_data: list[Transactions]) -> SExpenses:
        try:
            expenses_dict = {i.value: 0 for i in CatEnum}
            for i in trans_data:
                expenses_dict[i.cat.value] += i.price
            return SExpenses(**expenses_dict)
        except:
            logger.error("Ошибка при формировании словаря трат")