# Loans.py
from db import DB

class Loans(DB.Model):
    __tablename__ = "loans"
    id = DB.Column(DB.Integer, primary_key=True)
    CustID = DB.Column(DB.Integer, DB.ForeignKey('customers.id'), nullable=False) 
    BookID = DB.Column(DB.Integer, DB.ForeignKey('books.id'), nullable=False)    
    Loandate = DB.Column(DB.String(40), nullable=False)
    Returndate = DB.Column(DB.String(40), nullable=True)
    is_active = DB.Column(DB.Boolean, default=True)
    
    # Establish relationships using back_populates
    customer = DB.relationship('Customer', back_populates='loans', lazy=True)
    book = DB.relationship('Books', back_populates='loans', lazy=True)

    def __repr__(self):
        return f'<Loan id: {self.id}, CustID: {self.CustID}, BookID: {self.BookID}, LoanDate: {self.Loandate}, ReturnDate: {self.Returndate}>'