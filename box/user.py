from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime

from box.db import user, engine
from box.mess import Mess


# імпорт користувача з бази данних по user_id
def get_user(user_id) -> user:
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_user = User(user_id=row[0], name=row[1], username=row[2], born=datetime.strptime(row[3], "%m/%d/%Y, %H:%M:%S"))
    return l_user


# перевірка чи є користувач в базі данних
def extend_user(user_id) -> bool:
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# функція контролю користувача
def control_user(from_user) -> None:
    if extend_user(from_user.id):
        it_user = get_user(from_user.id)
        it_user.username = from_user.username
        if from_user.last_name is not None:
            it_user.name = from_user.first_name + " " + from_user.last_name
        else:
            it_user.name = from_user.first_name
        it_user.update()
    else:
        if from_user.last_name is not None:
            name = from_user.first_name + " " + from_user.last_name
        else:
            name = from_user.first_name
        Mess(user_id=from_user.id).insert()
        it_user = User(user_id=from_user.id,
                       name=name,
                       username=from_user.username)
        it_user.insert()


# Клас описуючий короткі відомості про користувача
class User:

    def __init__(self, user_id, name, username, born=None):
        self.user_id = user_id
        self.name = name
        self.username = username
        if born is not None:
            self.born = born
        else:
            self.born = datetime.now()

    # Запис в бд
    def insert(self) -> None:
        ins = user.insert().values(user_id=self.user_id,
                                   name=self.name,
                                   username=self.username,
                                   born=self.born.strftime("%m/%d/%Y, %H:%M:%S"))
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)

    # оновлення даних для бази данних
    def update(self) -> None:
        upd = update(user).where(user.c.user_id == self.user_id).values(name=self.name,
                                                                        username=self.username, )
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)
