# Customers.py
from db import DB

class Customer(DB.Model):
    __tablename__ = "customers"  # Changed to lowercase
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    city = DB.Column(DB.String(100), nullable=False)
    age = DB.Column(DB.Integer, nullable=False)
    email = DB.Column(DB.String(100), nullable=False)
    is_active = DB.Column(DB.Boolean, default=True)

    loans = DB.relationship('Loans', back_populates='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}, City: {self.city}, Email: {self.email}>'