import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, BufferedInputFile
import asyncio

# Включим логирование, чтобы видеть ошибки
logging.basicConfig(level=logging.INFO)

# ТОКЕН твоего бота (получить у @BotFather)
TOKEN = '8809490896:AAFNEyC8Vq8oiwcZQL0HUjH8CLQoGkpnjdY'

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        "👋 Привет! Я бот-определитель ID.\n\n"
        "Просто отправь мне:\n"
        "🖼️ Любое ФОТО (сжатое или файлом)\n"
        "😎 ПРЕМИУМ ЭМОДЗИ (кастомный смайлик от Telegram Premium)\n"
        "🎨 СТИКЕР\n\n"
        "Я пришлю тебе его file_id и unique_id."
    )

# 1. Обработчик ФОТОГРАФИЙ (обычные фото, которые пользователь отправляет)
@dp.message(lambda message: message.photo is not None)
async def handle_photo(message: Message):
    # Самое большое фото в группе (последний элемент списка)
    photo = message.photo[-1]
    file_id = photo.file_id
    file_unique_id = photo.file_unique_id
    
    # Отправляем ID пользователю
    await message.answer(
        f"🖼️ <b>Информация о фото:</b>\n"
        f"<code>file_id</code> = <code>{file_id}</code>\n"
        f"<code>file_unique_id</code> = <code>{file_unique_id}</code>",
        parse_mode="HTML"
    )
    
    # Дополнительно: можно скачать фото и сохранить (опционально)
    # file = await bot.get_file(file_id)
    # await bot.download_file(file.file_path, f"downloaded_photo_{file_unique_id}.jpg")

# 2. Обработчик СТИКЕРОВ
@dp.message(lambda message: message.sticker is not None)
async def handle_sticker(message: Message):
    sticker = message.sticker
    file_id = sticker.file_id
    file_unique_id = sticker.file_unique_id
    emoji = sticker.emoji if sticker.emoji else "без эмодзи"
    
    await message.answer(
        f"🎨 <b>Информация о стикере:</b>\n"
        f"Эмодзи стикера: {emoji}\n"
        f"<code>file_id</code> = <code>{file_id}</code>\n"
        f"<code>file_unique_id</code> = <code>{file_unique_id}</code>",
        parse_mode="HTML"
    )

# 3. Обработчик ПРЕМИУМ ЭМОДЗИ (кастомные смайлы)
# В Telegram Premium-эмодзи приходят как обычные сообщения, НО с типом 'text'
# и внутри есть сущность 'MessageEntityType.CUSTOM_EMOJI'
@dp.message()
async def handle_premium_emoji(message: Message):
    # Проверяем, есть ли в сообщении кастомные эмодзи
    if message.entities:
        for entity in message.entities:
            if entity.type == "custom_emoji":
                # Получаем ID премиум-эмодзи
                custom_emoji_id = entity.custom_emoji_id
                
                # Получаем весь текст, чтобы показать сам эмодзи
                emoji_text = message.text or ""
                
                await message.answer(
                    f"😎 <b>Найден Premium эмодзи!</b>\n"
                    f"Сам эмодзи: {emoji_text}\n"
                    f"<code>custom_emoji_id</code> = <code>{custom_emoji_id}</code>\n\n"
                    f"<i>Этот ID можно использовать для отправки эмодзи через бота (только если у пользователя есть Premium)</i>",
                    parse_mode="HTML"
                )
                return  # Завершаем, если нашли эмодзи
    
    # Если не фото, не стикер и не премиум-эмодзи
    await message.answer(
        "❌ Я не понял, что это.\n"
        "Пожалуйста, отправь мне: фото, стикер или премиум-эмодзи (кастомный смайлик)."
    )

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())