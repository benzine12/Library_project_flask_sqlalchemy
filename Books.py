# Books.py
from db import DB

class Books(DB.Model):
    __tablename__ = "books"  # Changed to lowercase
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    author = DB.Column(DB.String(100), nullable=False)
    year_published = DB.Column(DB.Integer, nullable=False)
    type = DB.Column(DB.Integer, nullable=False)
    is_active = DB.Column(DB.Boolean, default=True)

    loans = DB.relationship('Loans', back_populates='book', lazy=True)

    def __repr__(self):
        return f'<Book {self.name}, Author: {self.author}, Active: {self.is_active}>'