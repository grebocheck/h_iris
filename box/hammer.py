from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime, timedelta

from box.db import ham, engine

BAN_TYPE = "BAN"
MUTE_TYPE = "MUTE"


# Отримати всі активні покарання
def get_all_ham():
    mass = []
    get = ham.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        mass.append(Hammer(user_id=row[0],
                           admin_user_id=row[1],
                           start=row[2].strptime("%m/%d/%Y, %H:%M:%S"),
                           ham_type=row[3],
                           ham_time=row[4].strptime("%m/%d/%Y, %H:%M:%S"),
                           comment=row[5]))
    return mass


# імпорт покараного з бази даних
def get_ham(user_id: int):
    s = select([ham]).where(ham.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_ham = Hammer(user_id=row[0],
                   admin_user_id=row[1],
                   start=row[2].strptime("%m/%d/%Y, %H:%M:%S"),
                   ham_type=row[3],
                   ham_time=row[4].strptime("%m/%d/%Y, %H:%M:%S"),
                   comment=row[5])
    return l_ham


# Бан юзера в базі даних
def db_ban(user_id: int, admin_user_id: int, comment: str) -> None:
    it_ham = Hammer(user_id=user_id,
                    admin_user_id=admin_user_id,
                    start=datetime.now(),
                    ham_type=BAN_TYPE,
                    ham_time=datetime.now(),
                    comment=comment)
    it_ham.insert()


# Мут юзера в базі даних
def db_mute(user_id: int, admin_user_id: int, delta_time: timedelta, comment: str) -> None:
    it_ham = Hammer(user_id=user_id,
                    admin_user_id=admin_user_id,
                    start=datetime.now(),
                    ham_type=MUTE_TYPE,
                    ham_time=datetime.now()+delta_time,
                    comment=comment)
    it_ham.insert()


# Перевірка на бан
def extend_ban(user_id):
    s = select([ham]).where(ham.c.user_id == user_id).where(ham.c.ham_type == BAN_TYPE)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# Перевірка на мут
def extend_mute(user_id):
    s = select([ham]).where(ham.c.user_id == user_id).where(ham.c.ham_type == MUTE_TYPE)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# Розбан
def db_unban(user_id):
    if extend_ban(user_id):
        s = delete([ham]).where(ham.c.user_id == user_id).where(ham.c.ham_type == BAN_TYPE)
        conn = engine.connect()
        conn.execute(s)


# Розмут
def db_unmute(user_id):
    if extend_mute(user_id):
        s = delete([ham]).where(ham.c.user_id == user_id).where(ham.c.ham_type == MUTE_TYPE)
        conn = engine.connect()
        conn.execute(s)


def calculate_punish_time(td: timedelta):
    return datetime.now() + td  # формирует само время мута


def punish_time_patterns(m_time: int, measure: str):
    # функция для подсчета времени мута
    if measure == 'хв' or measure == 'хвилин':
        return calculate_punish_time(timedelta(minutes=m_time)).timestamp()

    elif measure == 'г' or measure == 'год' or measure == 'годин':
        return calculate_punish_time(timedelta(hours=m_time)).timestamp()

    elif measure == 'д' or measure == 'днів':
        return calculate_punish_time(timedelta(days=m_time)).timestamp()

    else:
        raise TypeError


class Hammer:
    def __init__(self, user_id, admin_user_id, start, ham_type, ham_time, comment):
        self.user_id = user_id
        self.admin_user_id = admin_user_id
        if start is not None:
            self.start = start
        else:
            self.start = datetime.now()
        self.ham_type = ham_type
        self.ham_time = ham_time
        self.comment = comment

    # Запис в бд
    def insert(self) -> None:
        ins = ham.insert().values(user_id=self.user_id,
                                  admin_user_id=self.admin_user_id,
                                  start=self.start.strftime("%m/%d/%Y, %H:%M:%S"),
                                  ham_type=self.ham_type,
                                  ham_time=self.ham_time.strftime("%m/%d/%Y, %H:%M:%S"),
                                  comment=self.comment)
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)
