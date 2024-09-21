from db import DB # Импортируем объект db из основного файла приложения

class Books(DB.Model):
    __tablename__ = "Books"
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    author = DB.Column(DB.String(100), nullable=False)
    year_published = DB.Column(DB.Integer, nullable=False)
    type = DB.Column(DB.Integer, nullable=False)

    def __repr__(self):
        return f'<Book {self.name}, Author: {self.author}>'