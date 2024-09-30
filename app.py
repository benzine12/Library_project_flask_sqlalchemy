from flask import Flask, jsonify, request
from Loans import Loans
from Books import Books
from Customers import Customer
from db import DB
from flask_cors import CORS

#initiate a flask aplication and sqlalchemy database
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

DB.init_app(app)

#test func to show if server is running property
@app.route('/', methods=['GET'])
def test():
    return {"test":"success"}

#func to add new customer
@app.route('/add_customer',methods=['POST'])
def add_customer():
    data = request.json
    new_customer = Customer(
        name=data['name'],
        city=data['city'],
        age=data['age'],
        email=data['email']
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

    # Look up the customer by name
    customer = Customer.query.filter_by(name=data['CustomerName']).first()
    if customer is None:
        return jsonify({"error": "Customer not found"}), 404

    # Check if the customer is inactive
    if not customer.is_active:
        return jsonify({"error": "Customer is inactive and cannot loan books"}), 400

    # Look up the book by name
    book = Books.query.filter_by(name=data['BookName']).first()
    if book is None:
        return jsonify({"error": "Book not found"}), 404

    # Check if the book is inactive
    if not book.is_active:
        return jsonify({"error": "Book is inactive and cannot be loaned"}), 400

    # Check if the book is already loaned out (active loan exists for the book)
    active_loan = Loans.query.filter_by(BookID=book.id, is_active=True).first()
    if active_loan:
        return jsonify({"error": "Book is already loaned out"}), 400

    new_loan = Loans(
        CustID=customer.id,  # Use the customer's ID
        BookID=book.id,      # Use the book's ID
        Loandate=data['Loandate'],
        Returndate=None,     # Since the book is being loaned, Returndate is None
        is_active=True       # Loan is active
    )
    DB.session.add(new_loan)
    DB.session.commit()
    return jsonify({"message": "Loan added"}), 201
#func that you update the retur date of the book in loans table
@app.route('/return_book/<int:id>', methods=['POST'])
def return_book(id):
    data = request.json
    loan = Loans.query.get(id)
    if loan and loan.is_active:
        loan.Returndate = data.get('Returndate')
        loan.is_active = False  # Set is_active to False since the book is returned
        DB.session.commit() 
        return jsonify({"message": "Return date updated, loan closed"}), 201
    elif loan and not loan.is_active:
        return jsonify({"message": "Loan is already closed"}), 400
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
        'type':book.type,
        'is_active': book.is_active
        } for book in all_books])

#func to show all customers
@app.route('/customers',methods=['GET'])
def get_Customers():
    all_Customers = Customer.query.all()
    return jsonify([{
        'id': customer.id,
        'name':customer.name,
        'city':customer.city,
        'age':customer.age,
        'email':customer.email,
        'is_active': customer.is_active
        } for customer in all_Customers])

@app.route('/loans', methods=['GET'])
def get_loans():
    all_loans = Loans.query.all()
    loans_data = []
    for loan in all_loans:
        loans_data.append({
            'id': loan.id,
            'CustID': loan.CustID,
            'CustomerName': loan.customer.name,
            'BookID': loan.BookID,
            'BookTitle': loan.book.name,
            'Loandate': loan.Loandate,
            'Returndate': loan.Returndate,
            'is_active': loan.is_active  # Ensure is_active is included
        })
    return jsonify(loans_data)

#func to deactivate a book
@app.route('/books/<int:id>/toggle-status', methods=['PUT'])
def toggle_book_status(id):
    book = Books.query.get(id)
    if book:
        book.is_active = not book.is_active
        DB.session.commit()
        status = 'activated' if book.is_active else 'deactivated'
        return jsonify({'message': f'book {status} successfully.', 'is_active': book.is_active}), 200
    else:
        return jsonify({'message': 'book does not exist.'}), 404
    
#func to deactivate a customer
@app.route('/customers/<int:id>/toggle-status', methods=['PUT'])
def toggle_customer_status(id):
    customer = Customer.query.get(id)
    if customer:
        customer.is_active = not customer.is_active
        DB.session.commit()
        status = 'activated' if customer.is_active else 'deactivated'
        return jsonify({'message': f'Customer {status} successfully.', 'is_active': customer.is_active}), 200
    else:
        return jsonify({'message': 'Customer does not exist.'}), 404

#starting point
if __name__ == '__main__':
    with app.app_context():
        DB.create_all()  
    app.run(debug=True) 
    