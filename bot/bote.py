import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from bot import bot_texts
import settings
from box.user import control_user, get_user
from box.mess import get_stat, get_mess

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
    text = get_stat(message.from_user.id)
    await message.reply(text)


@dp.message_handler(content_types=[ContentType.PHOTO,
                                   ContentType.VOICE,
                                   ContentType.VIDEO,
                                   ContentType.STICKER,
                                   ContentType.ANIMATION,
                                   ContentType.TEXT])
async def echo(message):
    control_user(message.from_user)
    mess = get_mess(message.from_user.id)
    if message.content_type == ContentType.PHOTO:
        mess.add_image()
    elif message.content_type == ContentType.VOICE:
        mess.add_audio()
    elif message.content_type == ContentType.VIDEO:
        mess.add_video()
    elif message.content_type == ContentType.STICKER:
        mess.add_stick()
    elif message.content_type == ContentType.ANIMATION:
        mess.add_gifes()
    else:
        mess.add_texts()
    # it_user = get_user(message.from_user.id)
    # await message.answer(it_user.born.strftime("%m/%d/%Y, %H:%M:%S"))
