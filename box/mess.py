from sqlalchemy import create_engine, MetaData, update, delete
from sqlalchemy.sql import select
from datetime import datetime

from box.db import mess, engine, meta


class Mess:

    def __init__(self, user_id, texts=0, audio=0, image=0, video=0):
        self.user_id = user_id
        self.texts = texts
        self.audio = audio
        self.image = image
        self.video = video

    # Запис в бд
    def insert(self) -> None:
        ins = mess.insert().values(user_id=self.user_id,
                                   texts=self.texts,
                                   audio=self.audio,
                                   image=self.image,
                                   video=self.video, )
        conn = engine.connect()
        conn.execute(ins)

    # збільшити
    def add_texts(self) -> None:
        self.texts += 1
        upd = update(mess).where(mess.c.user_id == self.user_id).values(texts=self.texts)
        conn = engine.connect()
        conn.execute(upd)
