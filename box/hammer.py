from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime, timedelta

from box.db import ham, engine

BAN_TYPE = "BAN"
MUTE_TYPE = "MUTE"


# імпорт покараного з бази даних
def get_ham(user_id: int):
    s = select([ham]).where(ham.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_ham = Hammer(user_id=row[0],
                   admin_user_id=row[1],
                   start=row[2].strptime(row[3], "%m/%d/%Y, %H:%M:%S"),
                   ham_type=row[3],
                   ham_time=row[4].strptime(row[3], "%m/%d/%Y, %H:%M:%S"))
    return l_ham


# Бан юзера в базі даних
def db_ban(user_id: int, admin_user_id: int) -> None:
    it_ham = Hammer(user_id=user_id,
                    admin_user_id=admin_user_id,
                    start=datetime.now(),
                    ham_type=BAN_TYPE,
                    ham_time=datetime.now())
    it_ham.insert()


# Мут юзера в базі даних
def db_mute(user_id: int, admin_user_id: int, delta_time: timedelta) -> None:
    it_ham = Hammer(user_id=user_id,
                    admin_user_id=admin_user_id,
                    start=datetime.now(),
                    ham_type=MUTE_TYPE,
                    ham_time=delta_time)
    it_ham.insert()


class Hammer:
    def __init__(self, user_id, admin_user_id, start, ham_type, ham_time):
        self.user_id = user_id
        self.admin_user_id = admin_user_id
        if start is not None:
            self.start = start
        else:
            self.start = datetime.now()
        self.ham_type = ham_type
        self.ham_time = ham_time

    # Запис в бд
    def insert(self) -> None:
        ins = ham.insert().values(user_id=self.user_id,
                                  admin_user_id=self.admin_user_id,
                                  start=self.start.strftime("%m/%d/%Y, %H:%M:%S"),
                                  ham_type=self.ham_type,
                                  ham_time=self.ham_time.strftime("%m/%d/%Y, %H:%M:%S"))
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)
