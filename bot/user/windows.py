from datetime import date, timedelta, timezone
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, Next
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput, TextInput
from bot.user.getters import get_confirmed_data
from bot.user.handlers import (cancel_logic, on_confirm, category_selected)
from bot.user.state import AddTransactionsState
from bot.dao.models import CatEnum


def get_category_window() -> Window:
    """Окно выбора категории траты."""
    return Window(
        Const("Выберите категорию траты:"),
        Group(
            *[Button(
                text=Const(str(i.value)),
                id=str(i.value),
                on_click=category_selected
            ) for i in CatEnum],
            Cancel(Const("Отмена"), on_click=cancel_logic),
            width=2
        ),
        state=AddTransactionsState.category
    )


def get_description_window() -> Window:
    """Окно выбора категории траты."""
    return Window(
        Const("Введите описание траты"),
        TextInput(id="description", on_success=Next()),
        state=AddTransactionsState.descriptions
    )


def get_price_window() -> Window:
    """Окно выбора категории траты."""
    return Window(
        Const("Введите сумму траты"),
        TextInput(id="price", on_success=Next(), type_factory=int),
        state=AddTransactionsState.price
    )


def get_confirmed_window() -> Window:
    return Window(
        Format("{confirmed_text}"),
        Group(
            Button(Const("Все верно"), id="confirm", on_click=on_confirm),
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
        ),
        state=AddTransactionsState.success,
        getter=get_confirmed_data
    )