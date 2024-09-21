from db import DB

class Loans(DB.Model):
    __tablename__ = "Loans"
    id = DB.Column(DB.Integer, primary_key=True) 
    CustID = DB.Column(DB.Integer, DB.ForeignKey('Customers.id'), nullable=False) 
    BookID = DB.Column(DB.Integer, DB.ForeignKey('Books.id'), nullable=False)  
    Loandate = DB.Column(DB.String(40), nullable=False) 
    Returndate = DB.Column(DB.String(40), nullable=True)

    def __repr__(self):
        return f'<Loan id: {self.id}, CustID: {self.CustID}, BookID: {self.Bookid}, LoanDate: {self.Loandate}, ReturnDate: {self.Returndate}>'