from datetime import date, timedelta, timezone
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, Next, SwitchTo, ListGroup
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput, TextInput
from bot.transactions.getters import get_transactions
from bot.transactions.handlers import cancel_logic, process_date_selected
from bot.transactions.state import GetTransactionsState
from bot.dao.models import CatEnum



def select_method_window() -> Window:
    return Window(
        Const("Выберите варианты просмотра статистики"),
        Group(
            SwitchTo(
                text=Const(str("Просмотр трат в определенный день")),
                id=str(1),
                state=GetTransactionsState.select_date
            ),
            SwitchTo(
                text=Const(str("Просмотр трат за определенный месяц")),
                id=str(1),
                state=GetTransactionsState.select_date
            ),
            Cancel(Const("Отмена"), on_click=cancel_logic),
            width=1
        ),
        state=GetTransactionsState.select_method
    )


def get_date_window() -> Window:
    """Окно выбора даты."""
    return Window(
        Const("Какой день вас интересует"),
        Calendar(
            id="cal",
            on_click=process_date_selected,
            config=CalendarConfig(
                firstweekday=0,
                timezone=timezone(timedelta(hours=3)),
                max_date=date.today()
            )
        ),
        Back(Const("Назад")),
        Cancel(Const("Отмена"), on_click=cancel_logic),
        state=GetTransactionsState.select_date,
    )


def get_trans_window() -> Window:
    """Окно выбора стола."""
    return Window(
        Format("{trans_list}"),
        Group(
            Back(Const("Назад")),
            Cancel(Const("Отмена"), on_click=cancel_logic),
            width=2
        ),
        getter=get_transactions,
        state=GetTransactionsState.transactions,
    )