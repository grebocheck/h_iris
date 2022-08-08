import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from bot import bot_texts
import settings
from box.user import control_user, get_user

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(bot_texts.help)


@dp.message_handler(commands=['stat'])
async def process_help_command(message: types.Message):
    text = bot_texts.get_stat(get_user(message.from_user.id))
    await message.reply(text)


@dp.message_handler(content_types=[ContentType.PHOTO,
                                   ContentType.VOICE,
                                   ContentType.VIDEO,
                                   ContentType.STICKER,
                                   ContentType.ANIMATION,
                                   ContentType.TEXT])
async def echo(message):
    control_user(message.from_user)
    it_user = get_user(message.from_user.id)
    if message.content_type == ContentType.PHOTO:
        it_user.add_image()
    elif message.content_type == ContentType.VOICE:
        it_user.add_audio()
    elif message.content_type == ContentType.VIDEO:
        it_user.add_video()
    elif message.content_type == ContentType.STICKER:
        it_user.add_stick()
    elif message.content_type == ContentType.ANIMATION:
        it_user.add_gifes()
    else:
        it_user.add_texts()
    # it_user = get_user(message.from_user.id)
    # await message.answer(it_user.born.strftime("%m/%d/%Y, %H:%M:%S"))
