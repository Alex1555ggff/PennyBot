from aiogram_dialog import Dialog
from bot.user.windows import (get_category_window,
                              get_description_window,
                              get_price_window,
                              get_confirmed_window)


add_transactions_dialog = Dialog(
    get_category_window(),
    get_price_window(),
    get_description_window(),
    get_confirmed_window(),
)