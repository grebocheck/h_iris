from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime, timedelta

import settings
from box.db import admin, engine

# rank 0 - ранг debug
# rank 1 - ранг модератора
# rank 2 - ранг адміна
# rank 3 - ранг головного адміна

set_rank_list = [1, 2]  # ранги що можна видати


# перевірка доступа
def guardian(user_id: int, rank: int) -> bool:
    if user_id in settings.SUPER_ADMINS:
        return True
    if extend_admin(user_id=user_id):
        it_admin = get_admin(user_id)
        if it_admin.rank >= rank:
            return True
    return False


# перевірка чи є користувач в базі данних
def extend_admin(user_id: int) -> bool:
    s = select([admin]).where(admin.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    if row is None:
        return False
    else:
        return True


# отримати адміна з бд
def get_admin(user_id: int):
    if user_id not in settings.SUPER_ADMINS:
        s = select([admin]).where(admin.c.user_id == user_id)
        conn = engine.connect()
        result = conn.execute(s)
        row = result.fetchone()
        l_admin = Admin(user_id=row[0],
                        born=datetime.strptime(row[1], "%m/%d/%Y, %H:%M:%S"),
                        rank=row[2])
    else:
        l_admin = Admin(user_id=user_id, rank=3)
    return l_admin


# отримати всіх адмінів з бд
def get_all_admin():
    mass = []
    get = admin.select()
    conn = engine.connect()
    result = conn.execute(get)
    for row in result:
        l_admin = Admin(user_id=row[0],
                        born=datetime.strptime(row[1], "%m/%d/%Y, %H:%M:%S"),
                        rank=row[2])
        mass.append(l_admin)
    for a in settings.SUPER_ADMINS:
        l_admin = Admin(user_id=a,
                        rank=3)
        mass.append(l_admin)
    return mass


# призначити адміном
def set_admin(user_id, rank, from_user_id) -> bool:
    if rank == 1 and guardian(from_user_id, settings.LVL_SET_MODER) or rank == 2 and guardian(from_user_id,
                                                                                              settings.LVL_SET_ADMIN):
        if extend_admin(user_id):
            it_admin = get_admin(user_id)
            fr_admin = get_admin(from_user_id)
            if fr_admin.rank > it_admin.rank:
                it_admin.update()
                return True
            else:
                return False
        else:
            it_admin = Admin(user_id=user_id,
                             rank=rank)
            it_admin.insert()
            return True
    else:
        return False


# видалити адміна
def del_admin(user_id, from_user_id) -> bool:
    it_admin = get_admin(user_id)
    if it_admin.rank == 1 and settings.LVL_DEL_MODER or it_admin.rank == 2 and settings.LVL_DEL_ADMIN:
        fr_admin = get_admin(from_user_id)
        if fr_admin.rank > it_admin.rank:
            it_admin = get_admin(user_id)
            it_admin.delete()
            return True
        else:
            return False
    else:
        return False


class Admin:

    def __init__(self, user_id, born=None, rank=0):
        self.user_id = user_id
        if born is None:
            self.born = datetime.now()
        else:
            self.born = born
        self.rank = rank

    # Запис в бд
    def insert(self) -> None:
        ins = admin.insert().values(user_id=self.user_id,
                                    born=self.born.strftime("%m/%d/%Y, %H:%M:%S"),
                                    rank=self.rank)
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)

    # Оновлення рангу
    def update(self) -> None:
        upd = update(admin).where(admin.c.user_id == self.user_id).values(rank=self.rank)
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)

    # Видалення адміна
    def delete(self) -> None:
        if extend_admin(self.user_id):
            dele = delete(admin).where(admin.c.user_id == self.user_id)
            conn = engine.connect()
            conn.execute(dele)
