import asyncio
import asyncpg
import logging
import configparser
from contextlib import asynccontextmanager

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Database:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.pool = None

    async def init_pool(self):
        """Инициализация пула подключений"""
        config = self._read_config()
        self.pool = await asyncpg.create_pool(
            user=config['DB_USER'],
            password=config['DB_PASSWORD'],
            database=config['DB_NAME'],
            host=config['DB_HOST'],
            port=config['DB_PORT'],
            min_size=int(config.get('MIN_POOL_SIZE', 1)),
            max_size=int(config.get('MAX_POOL_SIZE', 10))
        )
        logger.info("Подключение к базе данных установлено")

    def _read_config(self):
        """Чтение файла конфигурации"""
        config = configparser.ConfigParser()
        config.read(self.config_file)
        return config['database']

    @asynccontextmanager
    async def get_connection(self):
        """Получение подключения к базе данных"""
        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

    async def execute(self, query: str, *args):
        """Выполнение запроса без возврата результата (INSERT, UPDATE, DELETE)"""
        async with self.get_connection() as conn:
            try:
                await conn.execute(query, *args)
                logger.info(f"Запрос выполнен: {query}")
            except Exception as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def fetch(self, query: str, *args):
        """Выполнение SELECT-запроса и возврат результата"""
        async with self.get_connection() as conn:
            try:
                result = await conn.fetch(query, *args)
                logger.info(f"Запрос выполнен: {query}")
                return result
            except Exception as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def fetchrow(self, query: str, *args):
        """Выполнение SELECT-запроса и возврат одной строки"""
        async with self.get_connection() as conn:
            try:
                result = await conn.fetchrow(query, *args)
                logger.info(f"Запрос выполнен: {query}")
                return result
            except Exception as e:
                logger.error(f"Ошибка выполнения запроса: {e}")
                raise

    async def transaction(self):
        """Контекстный менеджер для управления транзакцией"""
        async with self.get_connection() as conn:
            async with conn.transaction():
                yield conn

    async def close(self):
        """Закрытие пула подключений"""
        await self.pool.close()
        logger.info("Подключение к базе данных закрыто")


# Пример использования модуля
async def main():
    db = Database('config.ini')
    await db.init_pool()

    # Выполнение запроса на добавление данных
    await db.execute("INSERT INTO users (name, age) VALUES ($1, $2)", "John", 30)

    # Получение данных
    rows = await db.fetch("SELECT * FROM users")
    for row in rows:
        print(row)

    # Закрытие пула подключений
    await db.close()

# Запуск примера
if __name__ == '__main__':
    asyncio.run(main())
