from db import DB # Импортируем объект db из основного файла приложения

class Customers(DB.Model):
    __tablename__ = "Customers"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    city = DB.Column(DB.String(100), nullable=False)
    age = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f'<Customer {self.name}, City: {self.city}>'