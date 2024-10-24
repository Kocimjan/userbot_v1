
import asyncio
from database import Database


async def main():
    db = Database('config.ini')
    db.init_engine()  # Инициализация движка

    # Выполнение запроса на добавление данных
    await db.execute("INSERT INTO users (name, age) VALUES (:name, :age)", {'name': 'John', 'age': 30})

    # Получение данных
    rows = await db.fetch("SELECT * FROM users")
    for row in rows:
        print(row)

    # Закрытие пула подключений
    await db.close()

# Запуск программы
if __name__ == '__main__':
    asyncio.run(main())
