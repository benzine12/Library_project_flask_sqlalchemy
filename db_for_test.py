# create_database.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение моделей
class Customers(db.Model):
    __tablename__ = 'Customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Customer {self.name}, City: {self.city}>'

class Books(db.Model):
    __tablename__ = 'Books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year_published = db.Column(db.Integer, nullable=False)
    type = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.name}, Author: {self.author}>'

class Loans(db.Model):
    __tablename__ = 'Loans'
    id = db.Column(db.Integer, primary_key=True)
    CustID = db.Column(db.Integer, db.ForeignKey('Customers.id'), nullable=False)
    Bookid = db.Column(db.Integer, db.ForeignKey('Books.id'), nullable=False)
    Loandate = db.Column(db.String(10), nullable=False)
    Returndate = db.Column(db.String(10), nullable=True)

    customer = db.relationship('Customers', backref=db.backref('loans', lazy=True))
    book = db.relationship('Books', backref=db.backref('loans', lazy=True))

    def __repr__(self):
        return f'<Loan CustomerID: {self.CustID}, BookID: {self.Bookid}>'

# Функция для заполнения базы данных данными
def populate_db():
    # Создаем клиентов
    customer1 = Customers(name='Иван Иванов', city='Москва', age=30)
    customer2 = Customers(name='Мария Смирнова', city='Санкт-Петербург', age=25)
    customer3 = Customers(name='Алексей Петров', city='Казань', age=40)

    db.session.add_all([customer1, customer2, customer3])
    db.session.commit()

    # Создаем книги с типами 1, 2 и 3
    book1 = Books(name='Война и мир', author='Лев Толстой', year_published=1869, type=1)
    book2 = Books(name='Преступление и наказание', author='Фёдор Достоевский', year_published=1866, type=2)
    book3 = Books(name='Мастер и Маргарита', author='Михаил Булгаков', year_published=1966, type=3)

    db.session.add_all([book1, book2, book3])
    db.session.commit()

    # Создаем займы
    loan1 = Loans(CustID=customer1.id, Bookid=book1.id, Loandate='2023-09-01', Returndate=None)
    loan2 = Loans(CustID=customer2.id, Bookid=book2.id, Loandate='2023-09-05', Returndate='2023-09-15')
    loan3 = Loans(CustID=customer3.id, Bookid=book3.id, Loandate='2023-09-10', Returndate=None)

    db.session.add_all([loan1, loan2, loan3])
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        populate_db()
        print("База данных успешно создана и заполнена данными.")