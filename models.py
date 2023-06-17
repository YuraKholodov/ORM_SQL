from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Numeric,
    Date,
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


Base = declarative_base()


class Publisher(Base):
    __tablename__ = "publishers"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"Publisher: {self.name}"


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    id_publisher = Column(Integer, ForeignKey("publishers.id", ondelete="CASCADE"))

    publisher = relationship("Publisher", backref="books")
    stock_shop = relationship("Shop", secondary="stocks", back_populates="stock_book")

    def __repr__(self):
        return f"Book: {self.title}"


class Shop(Base):
    __tablename__ = "shops"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    stock_book = relationship("Book", secondary="stocks", back_populates="stock_shop")

    def __repr__(self):
        return f"Shop: {self.name}"


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey("books.id"), nullable=False)
    id_shop = Column(Integer, ForeignKey("shops.id"), nullable=False)
    count = Column(Integer)


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True)
    price = Column(Numeric(10, 2))
    date_sale = Column(Date, default=datetime.now)
    id_stock = Column(Integer, ForeignKey("stocks.id"))
    count = Column(Integer)

    stock = relationship("Stock", backref="sales")


def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
