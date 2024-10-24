
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import logging
import configparser
from contextlib import asynccontextmanager
from sqlalchemy.exc import SQLAlchemyError

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.engine = None
        self.async_session = None

    def _read_config(self):
        """Чтение файла конфигурации"""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config['database']

    def init_engine(self):
        """Инициализация асинхронного движка с пулом подключений"""
        config = self._read_config()
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{config['DB_USER']}:{config['DB_PASSWORD']}@{config['DB_HOST']}:{config['DB_PORT']}/{config['DB_NAME']}",
            echo=True,  # Включить логирование SQL-запросов
            pool_size=int(config.get('POOL_SIZE', 10)),  # Размер пула
            max_overflow=int(config.get('MAX_OVERFLOW', 20))  # Максимальное количество дополнительных подключений
        )
        self.async_session = sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self):
        """Получение сессии для работы с базой данных"""
        async with self.async_session() as session:
            try:
                yield session
            except SQLAlchemyError as e:
                logger.error(f"Ошибка базы данных: {e}")
                raise

    async def execute(self, query: str, *args):
        """Выполнение SQL-запросов (INSERT, UPDATE, DELETE)"""
        async with self.get_session() as session:
            try:
                await session.execute(query, args)
                await session.commit()  # Подтверждение изменений
                logger.info(f"Запрос выполнен: {query}")
            except SQLAlchemyError as e:
                await session.rollback()
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def fetch(self, query: str, *args):
        """Выполнение SELECT-запроса и возврат результата"""
        async with self.get_session() as session:
            try:
                result = await session.execute(query, args)
                return result.fetchall()  # Получение всех строк
            except SQLAlchemyError as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def fetchrow(self, query: str, *args):
        """Выполнение SELECT-запроса и возврат одной строки"""
        async with self.get_session() as session:
            try:
                result = await session.execute(query, args)
                return result.fetchone()  # Получение одной строки
            except SQLAlchemyError as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def close(self):
        """Закрытие движка и пула подключений"""
        await self.engine.dispose()
        logger.info("Подключение к базе данных закрыто")
