import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from contextlib import suppress
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from bot import bot_texts
import settings
from box.user import control_user, get_user, extend_user
from box.hammer import db_ban, db_unban, db_mute, db_unmute, extend_ban, extend_mute, form_context
import asyncio

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


async def delete_message(message: types.Message, sleep_time: int = 0):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    it_mess = await message.reply(bot_texts.help, parse_mode="Markdown")

    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess, 20))


@dp.message_handler(commands=['profile'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    text = bot_texts.get_stat(get_user(message.from_user.id))
    it_mess = await message.reply(text, parse_mode="Markdown")
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess, 20))


@dp.message_handler(lambda message: bot_texts.get_chan(message.text) and message.reply_to_message)
async def carma(message: types.Message):
    control_user(message.from_user)
    if extend_user(message.reply_to_message.from_user.id):
        it_user = get_user(message.reply_to_message.from_user.id)
        if bot_texts.get_chan_in(message.text, '+') and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(True)
            it_mess = await message.reply(text=bot_texts.change_rep(it_user, True))
            if settings.AUTO_DELETE:
                asyncio.create_task(delete_message(it_mess, 20))
        elif bot_texts.get_chan_in(message.text, '-') and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(False)
            it_mess = await message.reply(text=bot_texts.change_rep(it_user, False))
            if settings.AUTO_DELETE:
                asyncio.create_task(delete_message(it_mess, 20))
        else:
            pass
    await echo(message)


@dp.message_handler(lambda message: bot_texts.bader(message.text))
async def bad(message: types.Message):
    await message.delete()
    it_mess = await message.answer(bot_texts.bad_word)
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess, 20))


@dp.message_handler(lambda message: message.reply_to_message, commands='report')
async def report_command(message: types.Message):
    control_user(message.from_user)
    admins = []  # тут будет список админов из бд
    for admin in admins:
        await bot.send_message(admin.user_id, f"")  # тут будет прямая ссылка на сообщение
    await message.delete()
    it_mes = await message.answer("Reported")

    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes, 20))


@dp.message_handler(lambda message: message.reply_to_message, commands='ban')
async def ban_command(message: types.Message):
    control_user(message.from_user)
    admin = {'rank': 2}  # тут будет получение админа и его ранга из бд, пока так
    if not admin:  # если админа не найдет то сразу выкинет
        it_mes = await message.answer('Нет прав')
        if settings.AUTO_DELETE:
            asyncio.create_task(delete_message(it_mes, 20))
        return
    user_to_ban = message.reply_to_message.from_user.id
    ban_mes = message.text.split()
    print(ban_mes)
    context = form_context(ban_mes, bot_texts.get_username(get_user(user_to_ban)))
    if context and admin["rank"] == 2:  # бан на втором ранге
        await bot.ban_chat_member(message.chat.id, user_to_ban)
        db_ban(user_to_ban, message.from_user.id)
        await message.delete()
        it_mes = await message.answer(bot_texts.show_admin_comment(context))
    else:
        it_mes = await message.answer('Что-то пошло не по плану\nВид бан сообщения: /ban мой коммент...')
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes, 20))


@dp.message_handler(lambda message: message.reply_to_message, commands='unban')
async def unban_command(message: types.Message):
    control_user(message.from_user)
    user_to_unban = message.reply_to_message.from_user.id
    admin = {'rank': 2}
    # тут в принцыпе всё то же самое ток с разбаном
    if not admin:
        it_mes = await message.answer('Нет прав')
        if settings.AUTO_DELETE:
            asyncio.create_task(delete_message(it_mes, 20))
        return
    if admin["rank"] == 2:
        await bot.unban_chat_member(message.chat.id, user_to_unban)
        db_unban(user_to_unban)
        it_mes = await message.answer("Пользователь разбанен")
    else:
        it_mes = await message.answer("Недостаточно прав")
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes, 20))


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
