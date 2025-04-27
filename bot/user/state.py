from aiogram.fsm.state import State, StatesGroup


class AddTransactionsState(StatesGroup):
    category = State()
    price = State()
    descriptions = State()
    success = State()