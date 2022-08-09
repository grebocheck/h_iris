import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from bot import bot_texts
import settings
from box.user import control_user, get_user, message_check

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN, parse_mode="Markdown")
dp = Dispatcher(bot)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    await message.reply(bot_texts.help)


@dp.message_handler(commands=['stat'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    text = bot_texts.get_stat(get_user(message.from_user.id))
    await message.reply(text)


@dp.message_handler(commands='carma_up')
async def carma_up_command(message: types.Message):
    control_user(message.from_user)
    user_change_rep = get_user(message.reply_to_message.from_user.id)
    user_change_rep.add_reput()
    await message.answer(bot_texts.show_rating(user_change_rep, "підвищено"))


@dp.message_handler(commands='carma_down')
async def carma_down_command(message: types.Message):
    control_user(message.from_user)
    user_change_rep = get_user(message.reply_to_message.from_user.id)
    user_change_rep.decr_reput()
    await message.answer(bot_texts.show_rating(user_change_rep, "знижено"))


@dp.message_handler(content_types=[ContentType.PHOTO,
                                   ContentType.VOICE,
                                   ContentType.VIDEO,
                                   ContentType.STICKER,
                                   ContentType.ANIMATION,
                                   ContentType.TEXT])
async def echo(message: types.Message):

    if message_check(message.text.lower(), bot_texts.bad_phrases):
        # вызываем проверку, если нашло очень плохое удаляем сразу
        await message.delete()

    else:
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
