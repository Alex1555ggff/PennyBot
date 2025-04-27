from aiogram_dialog import DialogManager
import datetime


async def get_confirmed_data(dialog_manager: DialogManager, **kwargs):
    """Получение данных для подтверждения."""
    cat = dialog_manager.dialog_data["cat"]
    description = dialog_manager.find("description").get_value()
    price = dialog_manager.find("price").get_value()

    confirmed_text = (
        "<b>📅 Подтверждение записи</b>\n\n"
        f"<b>📆 Дата:</b> {datetime.datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"<b>Информация о траты:</b>\n"
        f"  - 📝 Описание: {description}\n"
        f"  - 👥 Категория: {cat}\n"
        f"  - 📍 Цена: {price}\n\n"
        "✅ Все ли верно?"
    )

    return {"confirmed_text": confirmed_text}