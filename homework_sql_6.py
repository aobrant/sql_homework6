import psycopg2
import sqlalchemy
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import configparser
from pprint import pprint
import json

from models import create_tables, Publisher, Book, Sale, Shop, Stock

Base = declarative_base()

config = configparser.ConfigParser()
config.read("config.ini")
login = (config.get('PG','login'))[1:-1:]
password = (config.get('PG','password'))[1:-1:]
db = (config.get('PG','db'))[1:-1:]


DSN = f"postgresql://{login}:{password}@localhost:5432/{db}"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r') as td:
    data = json.load(td)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
    session.commit()

p_id = input ("Input publisher's id: ")
for q in session.query(Publisher).filter(Publisher.id == p_id).all():
    print(q)
for d in session.query(Book).join(Publisher.book).filter(Publisher.id == p_id).all():
        print(d)

subq = session.query(Book).join(Publisher.book).filter(Publisher.id == p_id).subquery()
subq2 = session.query(Stock).join(subq, Stock.id_book == subq.c.id).subquery()
for q in session.query(Shop).join(subq2, Shop.id == subq2.c.id_shop):
    print(q.name)


session.close()

