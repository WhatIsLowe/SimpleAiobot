import asyncio
import logging
import os
import sqlite3
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from dotenv import load_dotenv


# Импортируем .env файл
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')

dp = Dispatcher()

# Создаем базу данных SQLite для хранения chat_id подписавшихся пользователей
conn = sqlite3.connect('subscribers.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS subscribers (chat_id INTEGER PRIMARY KEY)")
conn.commit()

def is_subscriber(chat_id):
    """Проверка chat_id пользователя на наличие в базе

    Args:
        chat_id (str): id чата с пользователем
    """
    c.execute('SELECT chat_id FROM subscribers WHERE chat_id=?', (chat_id,))
    return c.fetchone() is not None

def subscribe(chat_id):
    """Заносит chat_id пользователя в базу

    Args:
        chat_id (str): id чата с пользователем
    """
    c.execute('INSERT OR IGNORE INTO subscribers (chat_id) VALUES (?)', (chat_id,))
    conn.commit()

def unsubscribe(chat_id):
    """Удаляет chat_id пользователя из базы

    Args:
        chat_id (str): id чата с пользователем
    """
    c.execute('DELETE FROM subscribers WHERE chat_id=?', (chat_id,))
    conn.commit()

# Обработчик команды /start
@dp.message(Command('subscribe', ignore_case=True))
async def start_message(message: types.Message):

    # Проверка, является ли пользователь подписчиком
    subscribed = is_subscriber(message.chat.id)

    # Создаем кнопку с текстом (подписаться/отписаться) и обратным вызовом
    button_text = 'Отписаться' if subscribed else "Подписаться на паука"
    callback_data = 'unsubscribe' if subscribed else 'subscribe'
    button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])#.add(button)

    # Отправка сообщения с кнопкой
    await message.answer('Нажмите на кнопку, чтобы подписаться или отписаться на паука', reply_markup=keyboard)

# Обработчик нажатия на кнопку
@dp.callback_query(lambda c: c.data in ['subscribe', 'unsubscribe'])
async def handle_button(callback_query: types.CallbackQuery):
    # Получаем данные из обратного вызова
    chat_id = callback_query.message.chat.id
    data = callback_query.data

    # Проверяем, подписаться или отписаться
    if data == 'subscribe':
        subscribe(chat_id)
        text = 'Вы успешно подписались!'
        button_text = 'Отписаться'
        callback_data = 'unsubscribe'
    else:
        unsubscribe(chat_id)
        text = 'Вы отписались'
        button_text = 'Подписаться на паука'
        callback_data = 'subscribe'

    # Обновляем текст кнопки
    button = InlineKeyboardButton(text=button_text, callback_data=callback_data)
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[button]])#.add(button)

    # Отправка сообщения с обновленной кнопкой и уведомление пользователя об успешной подписке/отписке
    await callback_query.answer(text=text)
    await callback_query.message.edit_reply_markup(str(callback_query.message.message_id), reply_markup=keyboard)

async def main():
    # Инициализируем бота с токеном
    bot = Bot(TOKEN)
    try:
        await dp.start_polling(bot)
        logging.log(logging.INFO, "Бот работает")
    except Exception as e:
        logging.log(logging.ERROR, f"Ошибка во время работы бота: {e}")


if __name__=='__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
