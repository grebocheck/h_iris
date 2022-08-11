import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ContentType

from contextlib import suppress
from aiogram.utils.exceptions import (MessageToEditNotFound, MessageCantBeEdited, MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from bot import bot_texts
import settings
from box.user import control_user, get_user, extend_user, get_user_by_name
from box.hammer import db_ban, db_unban, db_mute, db_unmute, extend_ban, extend_mute, get_ham, get_punish_time
import asyncio

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=settings.TOKEN)
dp = Dispatcher(bot)


# delete late message
async def delete_message(message: types.Message, sleep_time: int = settings.DEL_TIME):
    await asyncio.sleep(sleep_time)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await message.delete()


# HELP
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    it_mess = await message.answer(bot_texts.help, parse_mode="Markdown")

    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess))


# PROFILE
@dp.message_handler(commands=['profile'])
async def process_help_command(message: types.Message):
    control_user(message.from_user)
    text = bot_texts.get_stat(get_user(message.from_user.id))
    it_mess = await message.answer(text, parse_mode="Markdown")

    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess))


# REPORT
@dp.message_handler(lambda message: message.reply_to_message, commands='report')
async def report_command(message: types.Message):
    control_user(message.from_user)
    chat_url = message.chat.get_url()
    await bot.send_message(settings.ADMIN_GROUP, bot_texts.reported(m_id=message.reply_to_message.message_id,
                                                                    chat_url=chat_url,
                                                                    name=bot_texts.get_username(
                                                                        get_user(message.from_user.id))))
    it_mes = await message.answer(bot_texts.reported, parse_mode="Markdown")

    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes))


# BAN
@dp.message_handler(lambda message: message.reply_to_message, commands='ban')
async def ban_command(message: types.Message):
    control_user(message.from_user)
    if message.from_user.id in settings.SUPER_ADMINS:  # первый и высший админ чей id вписан в настройки
        user_to_ban = message.reply_to_message.from_user.id
        comment = message.text[5:]
        if comment == '':
            comment = "Нету"
        await bot.ban_chat_member(message.chat.id, user_to_ban)
        db_ban(user_id=user_to_ban,
               admin_user_id=message.from_user.id,
               comment=comment)
        it_mes = await message.answer(bot_texts.ham_text(get_ham(user_to_ban)), parse_mode="Markdown")
    else:
        it_mes = await message.answer(bot_texts.none_rights, parse_mode="Markdown")

    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes))


# UNBAN
@dp.message_handler(commands='unban')
async def unban_command(message: types.Message):
    control_user(message.from_user)
    if message.from_user.id in settings.SUPER_ADMINS:  # первый и высший админ чей id вписан в настройки
        name = message.text[7:]
        print(name)
        user_to_unban_pre = get_user_by_name(name)
        if user_to_unban_pre[0]:
            user_to_unban = user_to_unban_pre[1]
            await bot.unban_chat_member(message.chat.id, user_to_unban.user_id)
            db_unban(user_to_unban.user_id)
            it_mes = await message.answer(bot_texts.unbaned(user_to_unban), parse_mode="Markdown")
        else:
            it_mes = await message.answer(bot_texts.user_no, parse_mode="Markdown")
    else:
        it_mes = await message.answer(bot_texts.none_rights, parse_mode="Markdown")

    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes))


# MUTE
@dp.message_handler(lambda message: message.reply_to_message, commands='mute')
async def mute_command(message: types.Message):
    control_user(message.from_user)
    if message.from_user.id in settings.SUPER_ADMINS:
        user_to_mute = message.reply_to_message.from_user.id
        info = message.text.split()
        try:
            # ['/mute', '5', 'min', 'comment', 'comment']
            mute_dur = info[1:3]
            comment = ' '.join(info[3:]) if len(info) > 3 else 'Нету'
            # возвращает объект тайм-дельта
            delta_time = get_punish_time(mute_dur)
            await bot.restrict_chat_member(message.chat.id, user_to_mute, until_date=delta_time)
            db_mute(user_to_mute, message.from_user.id, delta_time, comment)
            it_mes = await message.answer(bot_texts.ham_text(get_ham(user_to_mute)))
        except IndexError:
            # сработает если команда введена неправильно
            it_mes = await message.answer(bot_texts.incor_command_form)
        except TypeError:
            # должно схватить ошибку в формировании времени
            it_mes = await message.answer(bot_texts.incor_time_mute)
    else:
        it_mes = await message.answer(bot_texts.none_rights)
    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes))


# UNMUTE
@dp.message_handler(commands='unmute')
async def unmute_command(message: types.Message):
    control_user(message.from_user)
    if message.from_user.id in settings.SUPER_ADMINS:
        try:
            name = message.text.split()[1]
            user_to_unmute_pre = get_user_by_name(name)
            if user_to_unmute_pre[0]:
                user_to_unmute = user_to_unmute_pre[1]
                # даёт разрешения пользователю, похоже размут делается так(надеюсь)
                await bot.restrict_chat_member(message.chat.id, user_to_unmute.user_id,
                                               can_send_messages=True,
                                               can_send_media_messages=True,
                                               can_send_other_messages=True)
                db_unmute(user_to_unmute.user_id)
                it_mes = await message.answer(bot_texts.unmuted(user_to_unmute))
            else:
                it_mes = await message.answer(bot_texts.user_no)
        except IndexError:
            # сработает если команда введена неправильно
            it_mes = await message.answer(bot_texts.incor_command_form)
    else:
        it_mes = await message.answer(bot_texts.none_rights)
    if settings.AUTO_DELETE_COMMAND:
        await message.delete()
    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mes))


# BAD PHRASE FILTER
@dp.message_handler(lambda message: bot_texts.bader(message.text))
async def bad(message: types.Message):
    await message.delete()
    it_mess = await message.answer(bot_texts.bad_word, parse_mode="Markdown")

    if settings.AUTO_DELETE:
        asyncio.create_task(delete_message(it_mess, 20))


# CHANGE REPUTATION
@dp.message_handler(lambda message: bot_texts.get_chan(message.text) and message.reply_to_message)
async def carma(message: types.Message):
    control_user(message.from_user)
    if extend_user(message.reply_to_message.from_user.id):
        it_user = get_user(message.reply_to_message.from_user.id)
        if bot_texts.get_chan_in(message.text, '+') and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(True)
            it_mess = await message.reply(text=bot_texts.change_rep(it_user, True), parse_mode="Markdown")
            if settings.AUTO_DELETE:
                asyncio.create_task(delete_message(it_mess, 20))
        elif bot_texts.get_chan_in(message.text, '-') and message.reply_to_message.from_user.id != message.from_user.id:
            it_user.change_reput(False)
            it_mess = await message.reply(text=bot_texts.change_rep(it_user, False), parse_mode="Markdown")
            if settings.AUTO_DELETE:
                asyncio.create_task(delete_message(it_mess))
        else:
            pass
    await echo(message)


# ANOTHER
@dp.message_handler(content_types=[ContentType.TEXT, ContentType.VIDEO, ContentType.VOICE,
                                   ContentType.AUDIO, ContentType.PHOTO, ContentType.ANIMATION,
                                   ContentType.STICKER, ContentType.VIDEO_NOTE])
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
