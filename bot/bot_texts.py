import settings
from box.user import get_user
from box.hammer import BAN_TYPE
from settings import APP_LANGUAGE
from datetime import datetime, timedelta

help = """Привет я помогу тебе розобраться с *ботом*
/report - уведомить *админов* о нарушении
/ban @username 3 Hour - Забанить на 3 часа (Day, Minute), для модератора не более 7 дней если не указано то навсегда (доступно только админу 2 ранга)
/mute @username 3 Hour - Замутить на 3 часа (Day, Minute), для модератора не более 2 дней
/stat - Статистика сообщений"""

bad_phrases = ['путин', "росия", "расия", "рассия", "россия", "руский", "русский",
               'русские', "руский", "руские"]  # словарь слов которые если видит удаляет сообщение


def bader(mess_text) -> bool:
    m_text = mess_text.split(" ")
    for a in m_text:
        if a.lower() in bad_phrases:
            return True
    return False


bad_word = "Такое говорить нельзя!"

not_replied = "Это не ответ на сообщение"

reported = "Уведомление силовым структурам чата отправлено!"

none_rights = "Недостаточно прав"

user_no = "Этого пользователя не найдено"

incor_command_form = "Неправильный формат команды"

incor_time_mute = "Возможно, неправильно введено время мута"

comment_max_warn = "Пользователь получил максимум варнов"

bad_add_admin = "Введите команду коректно /sadmin `число` , где 1-*модер*, 2-*админ*"

its_no_admin = "Выбраный пользователь не обладает правами администатора"


time_patterns = {
    'en': {
        'm': ['m', 'min', 'minute', 'minutes'],
        'h': ['h', 'hour', 'hours'],
        'd': ['d', 'day', 'days'],
    }
}


def del_admin(it_admin, from_admin):
    return f"{get_username(it_admin)} был лишён прав администатором {get_username(from_admin)}"


def set_admin(it_user, rank, admin):
    return f"{get_username(it_user)} получил администратора {rank} ранга от {get_username(admin)}"


def had_warns(it_user, admin):
    return f"{get_username(it_user)} получил варн *{it_user.warns}/{settings.MAX_WARNS} от {get_username(admin)}*"


def not_warns(it_user, admin):
    return f"{get_username(admin)} снял варн с {get_username(it_user)} *{it_user.warns}/{settings.MAX_WARNS}*"


def get_time_pattern(key, users_meas):
    return users_meas in time_patterns[APP_LANGUAGE][key]


def all_hams(ham_list):
    text = "`"
    if ham_list == []:
        text += "Активних покарань немає`"
    else:
        text += "ID".ljust(10) + "|" + "Имя".ljust(20) + "|" + "Админ".ljust(15) + "|" + "Тип".ljust(5) + "\n"
        for a in ham_list:
            text += str(a.user_id).ljust(10) + "|" + get_username(get_user(a.user_id)).ljust(20) + "|" \
                    + get_username(get_user(a.admin_user_id)).ljust(15) + "|" + a.ham_type.ljust(5) + "\n"
        text += "`"
    return text


def unbaned(it_user, admin) -> str:
    text = f"{get_username(admin)} розбанил {get_username(it_user)}"
    return text


def unmuted(it_user, admin) -> str:
    text = f"{get_username(admin)} розмутил {get_username(it_user)}"
    return text


def ham_text(HAMMER) -> str:
    if HAMMER.ham_type == BAN_TYPE:
        it_type = "Забанен"
        time_end = "Бан выдаеться навсегда"
    else:
        it_type = "Замученый"
        time_end = HAMMER.ham_time.strftime("%m/%d/%Y, %H:%M:%S")

    text = f"""Наказан пользователь {get_username(get_user(HAMMER.user_id))}
ID: `{HAMMER.user_id}`
Наказание: *{it_type}*
Наказал: {get_username(get_user(HAMMER.admin_user_id))}
Был заблокирован: _{HAMMER.start.strftime("%m/%d/%Y, %H:%M:%S")}_
Закончиться: _{time_end}_
Причина: *{HAMMER.comment}*
"""
    return text


def reporter(m_url, it_user):
    text = f"{get_username(it_user)} відправив репорт на <a href='{m_url}'>повідомлення</a>"
    return text


def get_chan(mess_text) -> bool:
    if mess_text[0] in ['+', '-']:
        return True
    return False


def get_chan_in(mess_text, res) -> bool:
    if mess_text[0] == res:
        return True
    return False


def get_username(it_user) -> str:
    if it_user.username is not None:
        name = "@" + it_user.username
    else:
        name = it_user.name
    return name


def get_stat(it_user) -> str:
    name = get_username(it_user)
    text = f"""Профиль {name}
*Репутация*: {it_user.reput}
*Варны*: {it_user.warns}/{settings.MAX_WARNS}
*В групе с*: {it_user.born.strftime("%m/%d/%Y, %H:%M:%S")}
Отправленые сообщения:
`Всего         {it_user.messages}
Текстов:      {it_user.texts}
Голосовых:    {it_user.audio}
Изображений:  {it_user.image}
Видео:        {it_user.video}
Стикеров:     {it_user.stick}
Гифок:        {it_user.gifes}`"""
    return text


def change_rep(it_user, change: bool) -> str:
    name = get_username(it_user)
    if change:
        text = f"{name}, ваша репутация увеличина на 1"
    else:
        text = f"{name}, ваша репутация уменьшена на 1"
    return text
