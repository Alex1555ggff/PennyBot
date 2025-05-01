from datetime import date, timedelta, timezone
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Group, ScrollingGroup, Select, Calendar, CalendarConfig, Back, Cancel, Next
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput, TextInput
from bot.user.getters import get_confirmed_data, get_transactions
from bot.user.handlers import (cancel_logic,
                               on_confirm,
                               category_selected,
                               process_date_selected,
                               process_transaction_selected)

from bot.user.state import AddTransactionsState, DeleteTransactionsState
from bot.dao.models import CatEnum


class CreateTransWindows:

    @classmethod
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

    @classmethod
    def get_description_window() -> Window:
        """Окно выбора категории траты."""
        return Window(
            Const("Введите описание траты"),
            TextInput(id="description", on_success=Next()),
            state=AddTransactionsState.descriptions
        )

    @classmethod
    def get_price_window() -> Window:
        """Окно выбора категории траты."""
        return Window(
            Const("Введите сумму траты"),
            TextInput(id="price", on_success=Next(), type_factory=int),
            state=AddTransactionsState.price
        )

    @classmethod
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
    

class DeleteTransactionsWindows:

    @classmethod
    def get_date_window() -> Window:
        """Окно выбора даты"""
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
        state=DeleteTransactionsState.select_date,
        )
    

    @classmethod
    def get_table_window() -> Window:
        """Окно выбора"""
        return Window(
            Format("{trans_list}"),
            ScrollingGroup(
                Select(
                    Format("{item[price]}-{item[description]}-{item[cat]}"),
                    id="trans_list",
                    item_id_getter=lambda item: str(item["id"]),
                    items="trans",
                    on_click=process_transaction_selected,
                ),
                id="tables_scrolling",
                width=1,
                height=3,
            ),
            Group(
                Back(Const("Назад")),
                Cancel(Const("Отмена"), on_click=cancel_logic),
                width=2
            ),
            getter=get_transactions,
            state=DeleteTransactionsState.select_trans,
        )