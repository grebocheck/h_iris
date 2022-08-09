from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime

from box.db import user, engine


# імпорт користувача з бази данних по user_id
def get_user(user_id: int):
    s = select([user]).where(user.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_user = User(user_id=row[0],
                  name=row[1],
                  username=row[2],
                  born=datetime.strptime(row[3], "%m/%d/%Y, %H:%M:%S"),
                  texts=row[4],
                  audio=row[5],
                  image=row[6],
                  video=row[7],
                  stick=row[8],
                  gifes=row[9],
                  reput=row[10])
    return l_user


# перевірка чи є користувач в базі данних
def extend_user(user_id: int) -> bool:
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
        it_user.update_user()
    else:
        if from_user.last_name is not None:
            name = from_user.first_name + " " + from_user.last_name
        else:
            name = from_user.first_name
        it_user = User(user_id=from_user.id,
                       name=name,
                       username=from_user.username)
        it_user.insert()


# Клас описуючий короткі відомості про користувача
class User:

    def __init__(self, user_id, name, username,
                 texts=0, audio=0, image=0, video=0, stick=0, gifes=0,
                 born=None, reput=0):

        self.user_id = user_id
        self.name = name
        self.username = username
        if born is not None:
            self.born = born
        else:
            self.born = datetime.now()
        self.texts = texts
        self.audio = audio
        self.image = image
        self.video = video
        self.stick = stick
        self.gifes = gifes
        self.reput = reput

    # Запис в бд
    def insert(self) -> None:
        ins = user.insert().values(user_id=self.user_id,
                                   name=self.name,
                                   username=self.username,
                                   born=self.born.strftime("%m/%d/%Y, %H:%M:%S"),
                                   texts=self.texts,
                                   audio=self.audio,
                                   image=self.image,
                                   video=self.video,
                                   stick=self.stick,
                                   gifes=self.gifes,
                                   reput=self.reput)
        conn = engine.connect()
        result = conn.execute(ins)
        print(result)

    # оновлення даних для бази данних
    def update_user(self) -> None:
        upd = update(user).where(user.c.user_id == self.user_id).values(name=self.name,
                                                                        username=self.username, )
        conn = engine.connect()
        result = conn.execute(upd)
        print(result)

    # збільшити texts
    def add_texts(self) -> None:
        self.texts += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(texts=self.texts)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити audio
    def add_audio(self) -> None:
        self.audio += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(audio=self.audio)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити image
    def add_image(self) -> None:
        self.image += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(image=self.image)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити video
    def add_video(self) -> None:
        self.video += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(video=self.video)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити stick
    def add_stick(self) -> None:
        self.stick += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(stick=self.stick)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити gifes
    def add_gifes(self) -> None:
        self.gifes += 1
        upd = update(user).where(user.c.user_id == self.user_id).values(gifes=self.gifes)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити репутацію
    def add_reput(self, add_min: bool) -> int:
        if add_min:
            self.reput += 1
        else:
            self.reput -= 1
        upd = update(user).where(user.c.user_id == self.user_id).values(gifes=self.reput)
        conn = engine.connect()
        conn.execute(upd)
        return self.reput
