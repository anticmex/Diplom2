from sqlalchemy import create_engine, MetaData, Table, Column, Integer, JSON, text
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("postgresql://chatbot:postgres@localhost/chatbotgroup")

DeclarativeBase = declarative_base()

def db_create():
    meta = MetaData()

    User = Table(
            'User', meta,
            Column('id', Integer, primary_key=True),
            Column('vk_id', Integer),
            Column('json', JSON)
        )

    try:
        db_user = text('SELECT * FROM public."User"')

        conn = engine.connect()
        result = conn.execute(db_user)
        print(result.fetchall())
    except:
        meta.create_all(engine)
        print('DB was created!')
