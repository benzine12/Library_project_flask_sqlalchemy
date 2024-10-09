Library Management System API

A RESTful API built with Flask for managing a library system, including functionalities to handle books, customers, and loans. This API allows for searching, adding, updating, and deactivating records, providing a comprehensive backend solution for library management.

Features

	•	Manage Books: Add, retrieve, update, and deactivate books.
	•	Manage Customers: Add, retrieve, update, and deactivate customer records.
	•	Handle Loans: Loan books to customers, return books, and track loan statuses.
	•	Search Functionality: Search for books by name or author and customers by name or email.
	•	CORS Enabled: Cross-Origin Resource Sharing enabled for frontend integration.
	•	SQLite Database: Simple and lightweight database setup using SQLite.

Technologies Used

	•	Flask: Web framework for building the API.
	•	Flask-CORS: Enables CORS for the Flask application.
	•	SQLAlchemy: ORM for database interactions.
	•	SQLite: Database used for storing data.
	•	Python 3.x: Programming language.

Installation

	1.	Clone the Repository

git clone https://github.com/yourusername/library-management-api.git
cd library-management-api


	2.	Create a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


	3.	Install Dependencies

pip install -r requirements.txt



Configuration

Ensure that the library.DB SQLite database is set up correctly. The database schema is managed via SQLAlchemy models defined in the Loans.py, Books.py, Customers.py, and db.py files.

Running the Application

	1.	Initialize the Database
The database tables are automatically created when you run the application for the first time.
	2.	Start the Flask Server

python app.py

The server will start on http://127.0.0.1:5000/ with debug mode enabled.

API Endpoints

Base URL

http://127.0.0.1:5000/

Health Check

	•	Endpoint: /
	•	Method: GET
	•	Description: Test if the server is running.
	•	Response:

{
  "test": "success"
}



Books

Get All Books

	•	Endpoint: /books
	•	Method: GET
	•	Description: Retrieve a list of all books.
	•	Response:

[
  {
    "id": 1,
    "name": "Book Title",
    "author": "Author Name",
    "year_published": 2020,
    "type": "Fiction",
    "is_active": true
  },
  ...
]



Get Book by ID

	•	Endpoint: /books/<int:id>
	•	Method: GET
	•	Description: Retrieve a specific book by its ID.
	•	Response:

{
  "id": 1,
  "name": "Book Title",
  "author": "Author Name",
  "year_published": 2020,
  "type": "Fiction",
  "is_active": true
}



Add a New Book

	•	Endpoint: /add_book
	•	Method: POST
	•	Description: Add a new book to the library.
	•	Request Body:

{
  "name": "Book Title",
  "author": "Author Name",
  "year_published": 2020,
  "type": "Fiction"
}


	•	Response:

{
  "message": "Book added"
}



Toggle Book Status

	•	Endpoint: /books/<int:id>/toggle-status
	•	Method: PUT
	•	Description: Activate or deactivate a book.
	•	Response:

{
  "message": "book deactivated successfully.",
  "is_active": false
}



Customers

Get All Customers

	•	Endpoint: /customers
	•	Method: GET
	•	Description: Retrieve a list of all customers.
	•	Response:

[
  {
    "id": 1,
    "name": "John Doe",
    "city": "New York",
    "age": 30,
    "email": "john.doe@example.com",
    "is_active": true
  },
  ...
]



Get Customer by ID

	•	Endpoint: /customers/<int:id>
	•	Method: GET
	•	Description: Retrieve a specific customer by their ID.
	•	Response:

{
  "id": 1,
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "email": "john.doe@example.com",
  "is_active": true
}



Add a New Customer

	•	Endpoint: /add_customer
	•	Method: POST
	•	Description: Add a new customer to the library system.
	•	Request Body:

{
  "name": "John Doe",
  "city": "New York",
  "age": 30,
  "email": "john.doe@example.com"
}


	•	Response:

{
  "message": "customer added"
}



Toggle Customer Status

	•	Endpoint: /customers/<int:id>/toggle-status
	•	Method: PUT
	•	Description: Activate or deactivate a customer.
	•	Response:

{
  "message": "Customer deactivated successfully.",
  "is_active": false
}



Loans

Get All Loans

	•	Endpoint: /loans
	•	Method: GET
	•	Description: Retrieve a list of all loans.
	•	Response:

[
  {
    "id": 1,
    "CustID": 1,
    "CustomerName": "John Doe",
    "BookID": 1,
    "BookTitle": "Book Title",
    "Loandate": "2023-01-01",
    "Returndate": null,
    "is_active": true
  },
  ...
]



Get Loan by ID

	•	Endpoint: /loans/<int:id>
	•	Method: GET
	•	Description: Retrieve a specific loan by its ID.
	•	Response:

{
  "id": 1,
  "CustID": 1,
  "CustomerName": "John Doe",
  "BookID": 1,
  "BookTitle": "Book Title",
  "Loandate": "2023-01-01",
  "Returndate": null,
  "is_active": true
}



Loan a Book

	•	Endpoint: /loan_book
	•	Method: POST
	•	Description: Create a new loan record for a customer and a book.
	•	Request Body:

{
  "CustomerName": "John Doe",
  "BookName": "Book Title",
  "Loandate": "2023-01-01"
}


	•	Response:

{
  "message": "Loan added"
}



Return a Book

	•	Endpoint: /return_book/<int:id>
	•	Method: POST
	•	Description: Update the return date of a loan and close the loan.
	•	Request Body:

{
  "Returndate": "2023-01-15"
}


	•	Response:

{
  "message": "Return date updated, loan closed"
}



Search

Search Books and Customers

	•	Endpoint: /search
	•	Method: GET
	•	Description: Search for books by name or author and customers by name or email.
	•	Query Parameter: q (the search term)
	•	Example: /search?q=John
	•	Response:

{
  "books": [
    {
      "id": 1,
      "name": "Book Title",
      "author": "Author Name",
      "year_published": 2020,
      "type": "Fiction",
      "is_active": true
    },
    ...
  ],
  "customers": [
    {
      "id": 1,
      "name": "John Doe",
      "city": "New York",
      "age": 30,
      "email": "john.doe@example.com",
      "is_active": true
    },
    ...
  ]
}



Project Structure

library-management-api/
│
├── app.py
├── Loans.py
├── Books.py
├── Customers.py
├── db.py
├── requirements.txt
├── README.md
└── library.DB

	•	app.py: Main Flask application containing all the API routes.
	•	Loans.py: SQLAlchemy model for loans.
	•	Books.py: SQLAlchemy model for books.
	•	Customers.py: SQLAlchemy model for customers.
	•	db.py: Database setup and configuration using SQLAlchemy.
	•	requirements.txt: Python dependencies.
	•	library.DB: SQLite database file.

Contributing

Contributions are welcome! Please follow these steps:

	1.	Fork the Repository
	2.	Create a New Branch

git checkout -b feature/YourFeature


	3.	Commit Your Changes

git commit -m "Add some feature"


	4.	Push to the Branch

git push origin feature/YourFeature


	5.	Open a Pull Request

License

This project is licensed under the MIT License.

Note: Ensure that you have the necessary models (Loans.py, Books.py, Customers.py, db.py) correctly defined for the application to work seamlessly.
