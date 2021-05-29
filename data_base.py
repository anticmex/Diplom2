from io import StringIO


import sqlalchemy.schema
from PIL.Image import Image
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.ddl import DropTable
from sqlalchemy.schema import DropTable
from sqlalchemy.ext.compiler import compiles


from data.creation_db import engine
from sqlalchemy import Column, text, MetaData, inspect, Table, schema, update, select, Integer, String, ForeignKey

'''meta = MetaData()
meta.reflect(bind=engine)
for table in reversed(meta.sorted_tables):
    print(table)
    #engine.execute(table.delete())
    #engine.execute(text(f'DROP TABLE IF EXISTS "{str(table)}";'))



base = declarative_base()
base.metadata.drop_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
'''

'''
a = MetaData().tables

print(a)
meta = MetaData().reflect(bind=engine)
print(MetaData().tables)
#base.metadata.drop_all(engine)
#print(base.metadata.tables.values())
session.commit()
session.close()
'''
metadata = MetaData()

metadata.reflect(bind=engine)
table_user = metadata.tables['User']
#table = metadata.tables
#print(len(engine.execute(table_user.select().where(table_user.c.vk_id == 1)).fetchall()))
#print(engine.execute(table_user.update().where(table_user.c.vk_id == 1).values(vk_id=133)))


meta = MetaData()
TestTable = Table(
    'TestTable', meta,
    Column('number', Integer, primary_key=True),
    Column('jpg', String, nullable=False)
    )
meta.create_all(engine)
#context = StringIO.StringIO()
im = open('dump/1.jpg', 'rb').read()
#print(im)

#engine.execute(meta.tables['TestTable'].insert().values(jpg=im))
#engine.execute(metadata.tables['TestTable'].insert().values(vk_id=19877))
outp = engine.execute(meta.tables['TestTable'].select()).fetchall()
print(len(outp))
for i in range(100):
    engine.execute(meta.tables['TestTable'].delete().where(meta.tables['TestTable'].c.number==i))
print(outp[9])
'''
for t in metadata.sorted_tables:
    print(metadata.tables)
    a = t.insert().values(vk_id=19877) #работает только это
    t.insert().values(vk_id=3)

    #engine.execute(a)
    data = engine.execute(t.select()).fetchall()
    print(engine.execute(t.select()).fetchall())
    print(data[0])
    engine.execute(t.delete().where(t.c.vk_id == 19838))#пашет
    print(engine.execute(t.select()).fetchall())#да, это огонь
    engine.execute(t.update().where(t.c.id_key == 3).values(id_key=2))  # пашет
    print(engine.execute(t.select().where(t.c.vk_id == 19877)).fetchall())  # да, это огонь
    #print(t.c.vk_id.text())
    t.insert().values(vk_id=4)

'''
'''Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
conn = engine.connect()
''''''
print(table)
#print(base.metadata.tables.values())

#metadata.remove['user']
table = metadata.tables


for n in metadata.sorted_tables:
    print(n)
    #a = update(n).values(ondelete='CASCADE')


    n.insert().values(vk_id=1932837)
    print(n.select)
    #print(engine.execute(n.delete()))
#declarative_base.metadata.insert()
print(metadata.tables)
''''''session.commit()
session.close()
'''#sqlalchemy_utils

'''
Base = automap_base()
Base.prepare(engine, reflect=True)
Users = Base.classes.user
session = Session(engine)
conn = engine.connect()
#res = session.query(Users).all()
conn.execute(DropTable(Table('Users', MetaData(), schema=schema)))
res = inspect(Users)
print(sqlalchemy.schema.DropTable)

#for r in res:
#    print(r)

print(res.all_orm_descriptors.keys())

'''

'''from sqlalchemy import MetaData
import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from base_code import engine

base = declarative_base()
metadata = MetaData()

class User(Base):
    __tablename__ = 'User'

    id = sq.Column(sq.INTEGER, primary_key=True)
    vk_id = sq.Column(sq.INTEGER)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    age = sq.Column(sq.INTEGER)
    range_age = sq.Column(sq.INTEGER)
    city = sq.Column(sq.String)


class DatingUser(Base):
    __tablename__ = 'DatingUser'

    id = sq.Column(sq.INTEGER, primary_key=True)
    vk_id = sq.Column(sq.INTEGER)
    first_name = sq.Column(sq.String)
    second_name = sq.Column(sq.String)
    age = sq.Column(sq.INTEGER)

    Users = relationship('User')
    id_User = sq.Column(sq.INTEGER, sq.ForeignKey('User.id'))


class Photos(Base):
    __tablename__ = 'Photos'

    id = sq.Column(sq.INTEGER, primary_key=True)
    link_photos = sq.Column(sq.String)
    count_likes = sq.Column(sq.INTEGER)

    Users = relationship('DatingUsers')
    id_DatingUser = sq.Column(sq.INTEGER, sq.ForeignKey('DatingUser.id'))

metadata.create_all(engine)
















































from lib2to3.pytree import Base
'''