from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime

from box.db import mess, engine, meta


def get_mess(user_id) -> mess:
    s = select([mess]).where(mess.c.user_id == user_id)
    conn = engine.connect()
    result = conn.execute(s)
    row = result.fetchone()
    l_mess = Mess(user_id=row[0], texts=row[1], audio=row[2], image=row[3], video=row[4])
    return l_mess


def get_stat(user_id) -> str:
    it_mess = get_mess(user_id)
    text = f"""Statistic
texts: {it_mess.texts}
audio: {it_mess.audio}
image: {it_mess.image}
video: {it_mess.video}
stick: {it_mess.stick}
gifes: {it_mess.gifes}"""
    return text


class Mess:

    def __init__(self, user_id, texts=0, audio=0, image=0, video=0, stick=0, gifes=0):
        self.user_id = user_id
        self.texts = texts
        self.audio = audio
        self.image = image
        self.video = video
        self.stick = stick
        self.gifes = gifes

    # Запис в бд
    def insert(self) -> None:
        ins = mess.insert().values(user_id=self.user_id,
                                   texts=self.texts,
                                   audio=self.audio,
                                   image=self.image,
                                   video=self.video,
                                   stick=self.stick,
                                   gifes=self.gifes)
        conn = engine.connect()
        conn.execute(ins)

    # збільшити texts
    def add_texts(self) -> None:
        self.texts += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(texts=self.texts)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити audio
    def add_audio(self) -> None:
        self.audio += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(audio=self.audio)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити image
    def add_image(self) -> None:
        self.image += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(image=self.image)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити video
    def add_video(self) -> None:
        self.video += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(video=self.video)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити stick
    def add_stick(self) -> None:
        self.stick += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(stick=self.stick)
        conn = engine.connect()
        conn.execute(upd)

    # збільшити gifes
    def add_gifes(self) -> None:
        self.gifes += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(gifes=self.gifes)
        conn = engine.connect()
        conn.execute(upd)
