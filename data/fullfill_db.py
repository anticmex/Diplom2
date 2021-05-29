from data.creation_db import engine
from sqlalchemy import MetaData


def db_fill(user_id, user_json):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_user = metadata.tables['User']
    user_select = engine.execute(table_user.select().where(table_user.c.vk_id == user_id)).fetchall()

    if len(user_select) > 0:
        return engine.execute(table_user.update().where(table_user.c.vk_id == user_id).values(json=user_json))
    else:
        return engine.execute(table_user.insert().values(vk_id=user_id, json=user_json))


def db_get(user_id):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_user = metadata.tables['User']
    return engine.execute(table_user.select().where(table_user.c.vk_id == user_id)).fetchall()


def db_del(user_id):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_user = metadata.tables['User']
    return engine.execute(table_user.delete().where(table_user.c.vk_id == user_id))
