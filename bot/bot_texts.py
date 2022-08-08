help = """Привет я помогу тебе розобраться с ботом
/report - уведомить админов
/ban @username 3 Hour - Забанить на 3 часа (Day, Minute), для модератора не более 7 дней если не указано то навсегда (доступно только админу 2 ранга)
/mute @username 3 Hour - Замутить на 3 часа (Day, Minute), для модератора не более 2 дней
/stat - Статистика сообщений"""


def get_stat(it_user) -> str:
    if it_user.username is not None:
        name = "@"+it_user.username
    else:
        name = it_user.name
    text = f"""Статистика {name}
`Текстов:     {it_user.texts}
Голосовых:   {it_user.audio}
Изображений: {it_user.image}
Видео:       {it_user.video}
Стикеров:    {it_user.stick}
Гифок:       {it_user.gifes}`"""
    return text