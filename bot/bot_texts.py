help = """Привет я помогу тебе розобраться с *ботом*
/report - уведомить *админов* о нарушении
/ban @username 3 Hour - Забанить на 3 часа (Day, Minute), для модератора не более 7 дней если не указано то навсегда (доступно только админу 2 ранга)
/mute @username 3 Hour - Замутить на 3 часа (Day, Minute), для модератора не более 2 дней
/stat - Статистика сообщений"""

bad_phrases = ['пидарас', "сука", "fack"]  # временный тестовый список


def bader(mess_text) -> bool:
    m_text = mess_text.split(" ")
    for a in m_text:
        if a in bad_phrases:
            return True
    return False


bad_word = "Такое говорить нельзя!"


def get_chan(mess_text) -> bool:
    m_text = mess_text.split(" ")
    if m_text[0] in ['+', '-']:
        return True
    return False


def get_chan_in(mess_text, res) -> bool:
    m_text = mess_text.split(" ")
    if m_text[0] == res:
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
