from enum import unique
import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


Base = declarative_base()

class Publisher(Base):
    __tablename__="publisher"

    id = sq.Column(sq.Integer,primary_key=True)
    name = sq.Column(sq.String(length=40),unique=True)

    def __str__(self) -> str:
        return f'Publisher {self.id}: {self.name} '

class Book(Base):
     __tablename__="book"

     id = sq.Column(sq.Integer,primary_key=True)
     title = sq.Column(sq.String(length=40),unique=True)
     id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

     publisher = relationship(Publisher, backref="book")

     def __str__(self) -> str:
        return f'Book: {self.id}: {self.title} '

class Shop(Base):
    __tablename__="shop"

    id = sq.Column(sq.Integer,primary_key=True)
    name = sq.Column(sq.String(length=40),unique=True)

class Stock(Base):
    __tablename__="stock"

    id = sq.Column(sq.Integer,primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)
    book = relationship(Book, backref="stock")
    shop = relationship(Shop, backref="stock")

class Sale(Base):
    __tablename__="sale"

    id = sq.Column(sq.Integer,primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.DateTime, nullable=True)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer, nullable=True)

    stock = relationship(Stock, backref="sale")
    

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

