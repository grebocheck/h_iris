import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType
from aiogram.dispatcher import filters

from bot import bot_texts
import settings
from box.user import control_user, get_user, extend_user

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    await message.reply(bot_texts.help, parse_mode="Markdown")


@dp.message_handler(commands=['profile'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    text = bot_texts.get_stat(get_user(message.from_user.id))
    await message.reply(text, parse_mode="Markdown")


@dp.message_handler(filters.Text(contains=['+'], ignore_case=True),
                    filters.Text(contains=['-'], ignore_case=True),
                    lambda message: message.reply_to_message)
async def carma(message: types.Message):
    control_user(message.from_user)
    if extend_user(message.reply_to_message.from_user.id):
        it_user = get_user(message.reply_to_message.from_user.id)
        if message.text in ["+"] and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(True)
            await message.reply(text=bot_texts.change_rep(it_user, True))
        elif message.text in ["-"] and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(False)
            await message.reply(text=bot_texts.change_rep(it_user, False))
        else:
            pass
    await echo(message)


@dp.message_handler(lambda message: bot_texts.bader(message.text))
async def bad(message: types.Message):
    await message.delete()
    await message.answer(bot_texts.bad_word)


@dp.message_handler(content_types=[ContentType.PHOTO,
                                   ContentType.VOICE,
                                   ContentType.VIDEO,
                                   ContentType.STICKER,
                                   ContentType.ANIMATION,
                                   ContentType.TEXT])
async def echo(message: types.Message):
    control_user(message.from_user)
    it_user = get_user(message.from_user.id)
    it_user.add_message()
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
