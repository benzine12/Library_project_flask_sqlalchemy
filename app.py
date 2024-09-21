from flask import Flask, jsonify, request
from Loans import Loans
from Books import Books
from Customers import Customers
from db import DB

#initiate a flask aplication and sqlalchemy database
app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

DB.init_app(app)

#test func to show if server is running property
@app.route('/test', methods=['GET'])
def test():
    return {"test":"success"}

#func to add new customer
@app.route('/add_customer',methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customers(
        name=data['name'],
        city=data['city'],
        age=data['age']
        )
    DB.session.add(new_customer)
    DB.session.commit()
    return jsonify({"message": 'customer added'}),201

#func to add a book
@app.route('/add_book',methods=['POST'])
def add_book():
    data = request.json
    new_book = Books(
        name=data['name'],
        author=data['author'],
        year_published=data['year_published'],
        type=data['type']
        )
    DB.session.add(new_book)
    DB.session.commit()
    return jsonify({"message": 'Book added'}),201

#func to add a new loan with book id and customer id
@app.route('/loan_book', methods=['POST'])
def loan_book():
    data = request.json
    customer = Customers.query.filter_by(id=data['CustID']).first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404
    
    book = Books.query.filter_by(id=data['BookID']).first()
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    new_loan = Loans(
        CustID=data['CustID'],
        BookID=data['BookID'],
        Loandate=data['Loandate'],
        Returndate=data.get('Returndate')  # Может быть None
    )
    DB.session.add(new_loan)
    DB.session.commit()
    return jsonify({"message": "Loan added"}), 201

#func that you update the retur date of the book in loans table
@app.route('/return_book/<int:id>', methods=['PUT'])
def return_book(id):
    data = request.json
    loan = Loans.query.get(id)
    if loan:
        loan.Returndate = data.get('Returndate')
        DB.session.commit() 
        return jsonify({"message": "Return date updated"}), 201
    else:
        return jsonify({"message": "Loan not found"}), 404

#func to show all books
@app.route('/books',methods=['GET'])
def get_Books():
    all_books = Books.query.all()
    return jsonify([{
        'id': book.id,
        'name':book.name,
        'author':book.author,
        'year_published':book.year_published,
        'type':book.type 
        } for book in all_books])

#func to show all customers
@app.route('/customers',methods=['GET'])
def get_Customers():
    all_Customers = Customers.query.all()
    return jsonify([{
        'id': customer.id,
        'name':customer.name,
        'city':customer.city,
        'age':customer.age,
        } for customer in all_Customers])

#func to show all loans 
@app.route('/loans',methods=['GET'])
def get_loans():
    all_loans = Loans.query.all()
    return jsonify([{
        'id': loan.id,
        'CustID':loan.CustID,
        'BookID':loan.BookID,
        'Loandate':loan.Loandate,
        'Returndate':loan.Returndate,
        } for loan in all_loans])

#func to delete a book
@app.route('/del_book/<int:id>',methods=['DELETE'])
def del_book(id):
    book = Books.query.get(id)
    if book:
        DB.session.delete(book)
        DB.session.commit()
        return jsonify({'message':'book deleted'})
    else:
        return jsonify({'message':'book does not exist'},404)

#func to delete a loan
@app.route('/del_loan/<int:id>',methods=['DELETE'])
def del_loan(id):
    loan = Loans.query.get(id)
    if loan:
        DB.session.delete(loan)
        DB.session.commit()
        return jsonify({'message':'loan deleted'})
    else:
        return jsonify({'message':'loan does not exist'},404)

#starting point
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()  
    app.run(debug=True) 
    