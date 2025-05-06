import os
import django
import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from asgiref.sync import sync_to_async

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testapp.settings')
django.setup()

from checkadmin.models import TelegramSubscriber, AdminNotification

API_TOKEN = 'Токен бота.'

logging.basicConfig(level=logging.INFO)  # Логирование в консоль.

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Клавиатура с единственной кнопкой для удобства.
subscribe_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Подписаться")]],
    resize_keyboard=True,
    one_time_keyboard=True
)


@dp.message(F.text == '/start')
async def cmd_start(message: Message):
    """Обработчик команды /start. Выводит на экран клавиатуру."""
    await message.answer(
        "Нажмите кнопку ниже, чтобы подписаться на уведомления.",
        reply_markup=subscribe_kb
    )


@dp.message(F.text == "Подписаться")
async def subscribe_handler(message: Message):
    """
    Проверка подписки пользователя на уведомления.
    Если пользователь новый, добавляет его в базу.
    Если пользователь есть в базе, игнориует и уведомляет что уже есть подписка.
    """
    chat_id = message.chat.id
    exists = await sync_to_async(TelegramSubscriber.objects.filter(chat_id=chat_id).exists)()
    if not exists:
        await sync_to_async(TelegramSubscriber.objects.create)(chat_id=chat_id)
        await message.answer("Вы успешно подписались на уведомления!", reply_markup=None)
    else:
        await message.answer("Вы уже подписаны на уведомления.", reply_markup=None)


async def notify_loop():
    """Бот читает данные из модели, и делает рассылку."""
    while True:
        notifications = await sync_to_async(list)(AdminNotification.objects.filter(sent=False))
        if notifications:
            subscribers = await sync_to_async(list)(TelegramSubscriber.objects.all())
            for notif in notifications:
                for sub in subscribers:  # Цикл по подписчикам.
                    try:
                        await bot.send_message(sub.chat_id, notif.text)
                    except Exception as e:
                        logging.error(f"Не удалось отправить сообщение {sub.chat_id}: {e}")
                notif.sent = True
                await sync_to_async(notif.save)()
        await asyncio.sleep(3)


async def main():
    """Запуск полинга."""
    asyncio.create_task(notify_loop())
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
