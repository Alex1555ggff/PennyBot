from aiogram_dialog import Dialog
from bot.transactions.windows import (
    get_date_window,
    get_trans_window,
    select_method_window,
)


get_transactions_dialog = Dialog(
    select_method_window(),
    get_date_window(),
    get_trans_window(),
)