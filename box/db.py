from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Boolean
import settings

# engine = create_engine('sqlite:///bot.db', echo=True)
engine = create_engine(settings.DATABASE, echo=True)
meta = MetaData()

user = Table(
    'user', meta,
    Column('user_id', Integer, primary_key=True),   # 0
    Column('name', String),                         # 1
    Column('username', String),                     # 2
    Column('born', String),                         # 3
    Column('texts', Integer),                       # 4
    Column('audio', Integer),                       # 5
    Column('image', Integer),                       # 6
    Column('video', Integer),                       # 7
    Column('stick', Integer),                       # 8
    Column('gifes', Integer),                       # 9
    Column('reput', Integer),                       # 10
    Column('messages', Integer),                    # 11
    Column('warns', Integer),                       # 12
    Column('warnborn', String),                     # 13
)

ham = Table(
    'ban', meta,
    Column('user_id', Integer),
    Column('admin_user_id', Integer),
    Column('start', String),
    Column('ham_type', String),
    Column('ham_time', String),
    Column('comment', String),
)

admin = Table(
    'admin', meta,
    Column('user_id', Integer),
    Column('born', String),
    Column('rank', Integer),
)

if __name__ == '__main__':
    meta.create_all(engine)
