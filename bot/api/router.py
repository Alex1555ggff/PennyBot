from datetime import datetime, timedelta
from faststream.rabbit.fastapi import RabbitRouter
from loguru import logger
from bot.create_bot import bot
from bot.config import settings, scheduler
from bot.dao.database import async_session_maker


router = RabbitRouter(url=settings.RABBITMQ_URL)


@router.subscriber("admin_msg")
async def send_booking_msg(msg: str):
    for admin in settings.ADMIN_IDS:
        await bot.send_message(admin, text=msg)


async def send_user_msg(user_id: int, text: str):
    await bot.send_message(user_id, text=text)


@router.subscriber("noti_user")
async def schedule_user_notifications(user_id: int):
    """Планирует отправку серии сообщений пользователю с разными интервалами."""
    now = datetime.now()

    notifications = [
        {
            "time": now + timedelta(minutes=1),
            "text": "Пока тест",
        },
    ]

    for i, notification in enumerate(notifications):
        job_id = f"user_notification_{user_id}_{i}"
        scheduler.add_job(
            send_user_msg,
            "date",
            run_date=notification["time"],
            args=[user_id, notification["text"]],
            id=job_id,
            replace_existing=True,
        )
        logger.info(
            f"Запланировано уведомление для пользователя {user_id} на {notification['time']}"
        )