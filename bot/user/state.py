from aiogram.fsm.state import State, StatesGroup


class AddTransactionsState(StatesGroup):
    category = State()
    price = State()
    descriptions = State()
    success = State()


class DeleteTransactionsState(StatesGroup):
    select_date = State()
    select_trans = State()