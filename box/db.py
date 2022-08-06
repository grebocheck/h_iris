from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
from loge import log

engine = create_engine('sqlite:///bot.db', echo=True)
meta = MetaData()

user = Table(
    'user', meta,
    Column('user_id', Integer, primary_key=True),
    Column('name', String),
    Column('username', String),
    Column('born', String),
)

mess = Table(
    'mess', meta,
    Column('user_id', Integer, primary_key=True),
    Column('texts', Integer),
    Column('audio', Integer),
    Column('image', Integer),
    Column('video', Integer),
)

ban = Table(
    'ban', meta,
    Column('user_id', Integer, primary_key=True),
    Column('start', String),
    Column('end', String),
)

mute = Table(
    'mute', meta,
    Column('user_id', Integer, primary_key=True),
    Column('start', String),
    Column('end', String),
)

admin = Table(
    'admin', meta,
    Column('user_id', Integer, primary_key=True),
    Column('born', String),
    Column('rank', Integer),
)

rep = Table(
    'rep', meta,
    Column('user_id', Integer, primary_key=True),
    Column('amount', Integer)
)


if __name__ == '__main__':
    meta.create_all(engine)
    log("Запущено db.py в режимі main")