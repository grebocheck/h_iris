import logging
from aiogram import Bot, Dispatcher, types

import bot_texts
import settings
from box.user import User, control_user, get_user

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def echo(message: types.Message):
    control_user(message.from_user)
    it_user = get_user(message.from_user.id)
    await message.answer(it_user.born.strftime("%m/%d/%Y, %H:%M:%S"))


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(bot_texts.help)