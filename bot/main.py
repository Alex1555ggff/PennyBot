from contextlib import asynccontextmanager
from bot.create_bot import dp, start_bot, bot, stop_bot
from bot.config import settings, broker, scheduler
from aiogram.types import Update
from fastapi import FastAPI, Request
from loguru import logger
from bot.api.router import router as router_fast_stream

@asynccontextmanager
async def lifespan(app: FastAPI):
    await start_bot()
    logger.info("Бот запущен...")
    await broker.start()
    logger.info("Брокер успешно запущен")
    scheduler.start()
    logger.info("Шелдер запушен")

    try:
        await bot.set_webhook(
            url=settings.hook_url,
            allowed_updates=dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        logger.info(f"Хук создан на url={settings.hook_url}")
    except Exception as e:
        logger.error(f"Ошибка запуска вебхука на urn{settings.hook_url}\n {e}")

    yield
    logger.info("Бот остановлен...")
    await stop_bot()
    await broker.close()
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logger.info("Получен запрос с вебхука.")
    try:
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot, update)
        logger.info("Обновление успешно обработано.")
    except Exception as e:
        logger.error(f"Ошибка при обработке обновления с вебхука: {e}")


app.include_router(router_fast_stream)