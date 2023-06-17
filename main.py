import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from sqlalchemy import or_

from models import Book, Publisher, Sale, Shop, Stock, create_tables


DSN = f"postgresql://postgres:baraguz@localhost:5432/books_db"
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()

# Наполняем базу из JSON

with open("tests_data.json", encoding="utf-8") as file:
    data = json.load(file)
    for row in data:
        model = row["model"].capitalize()
        temp = locals()[model](**row["fields"])
        session.add(temp)
        session.commit()


def find_publisher(data):
    """Функция поиска Автора"""
    query = session.query(
        Publisher.name, Book.title, Shop.name, Sale.price * Stock.count, Sale.date_sale
    )
    query = query.join(Book, Book.id_publisher == Publisher.id)
    query = query.join(Stock, Stock.id_book == Book.id)
    query = query.join(Shop, Shop.id == Stock.id_shop)
    query = query.join(Sale, Sale.id_stock == Stock.id)

    if data.isdigit():
        records = query.filter(Publisher.id == data)
    else:
        records = query.filter(Publisher.name == data)

    for name_publisher, title, shop, price, date in records:
        print(f"{name_publisher} | {title} | {shop} | {price} | {date}")


def test():
    query = session.query(Book)
    records = query.all()

    for i in records:
        print(i.title, i.publisher.name, i.stock_shop)


session.close()

if __name__ == "__main__":
    find_publisher(data=input("Введите имя автора или ID автора: "))

    # test()
