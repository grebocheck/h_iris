help = """Привет я помогу тебе розобраться с *ботом*
/report - уведомить *админов* о нарушении
/ban @username 3 Hour - Забанить на 3 часа (Day, Minute), для модератора не более 7 дней если не указано то навсегда (доступно только админу 2 ранга)
/mute @username 3 Hour - Замутить на 3 часа (Day, Minute), для модератора не более 2 дней
/stat - Статистика сообщений"""


bad_phrases = ['pay-me', "рішення прийнято"]  # временный тестовый список


def get_username(it_user):
    if it_user.username is not None:
        name = "@" + it_user.username
    else:
        name = it_user.name
    return name


def get_stat(it_user) -> str:
    name = get_username(it_user)
    text = f"""Статистика {name}
`Текстов:      {it_user.texts}
Голосовых:    {it_user.audio}
Изображений:  {it_user.image}
Видео:        {it_user.video}
Стикеров:     {it_user.stick}
Гифок:        {it_user.gifes}`"""
    return text


def show_rating(it_user, incr_decr) -> str:
    name = get_username(it_user)
    text = f"""Рейтинг користувача {name} було {incr_decr} на 1
Тепер він дорівнює {it_user.reput}"""  # вот тут хз сработает ли на актуальное количество репы, или надо
    # ещё переменную передать
    return text
