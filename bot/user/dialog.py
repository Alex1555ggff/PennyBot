from aiogram_dialog import Dialog
from bot.user.windows import CreateTransWindows


add_transactions_dialog = Dialog(
    CreateTransWindows.get_category_window(),
    CreateTransWindows.get_price_window(),
    CreateTransWindows.get_description_window(),
    CreateTransWindows.get_confirmed_window(),
)


delete_transactions_dialog = Dialog(
    
)