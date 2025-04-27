from aiogram.fsm.state import State, StatesGroup


class GetTransactionsState(StatesGroup):
    select_method = State()
    select_date = State()
    transactions = State()

