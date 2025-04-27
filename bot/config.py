import os
import requests
from typing import List
from urllib.parse import quote
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from faststream.rabbit import RabbitBroker
from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: List[int]
    DB_URL: str
    STORE_URL: str 
    LOG_ROTATION: str = "10 MB"
    FORMAT_LOG: str = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"

    REDIS_URL: str
    RABBITMQ_URL: str


    @property
    def BASE_URL(self) -> str:
        try:
            resp = requests.get("http://ngrok:4040/api/tunnels")
            tunnels = resp.json()["tunnels"]
            for tunnel in tunnels:
                if tunnel["proto"] == "https":
                    return tunnel["public_url"]
        except Exception as e:
            logger.error(f"Ошибка получения ngrok URL: {e}")
        return None


    @property
    def hook_url(self) -> str:
        """Возвращает URL вебхука"""
        return f"{self.BASE_URL}/webhook"

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


# Инициализация конфигурации
settings = Settings()

# Настройка логирования
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "log.txt")
logger.add(log_file_path, format=settings.FORMAT_LOG, level="INFO", rotation=settings.LOG_ROTATION)


logger.info(f"Создание брокера по url={settings.RABBITMQ_URL}")
# Создание брокера сообщений RabbitMQ
broker = RabbitBroker(settings.RABBITMQ_URL)

# Создание планировщика задач
scheduler = AsyncIOScheduler(jobstores={'default': SQLAlchemyJobStore(url=settings.STORE_URL)})