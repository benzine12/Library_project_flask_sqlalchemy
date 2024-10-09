# Library Management System

This project is a Library Management System built with Flask and SQLAlchemy. It provides a RESTful API for managing books, customers, and loans in a library setting.

## Features

- Add, view, and manage books
- Add, view, and manage customers
- Create and manage book loans
- Search functionality for books and customers
- Toggle active status for books and customers

## Prerequisites

- Python 3.x
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/benzine12/Library_project_flask_sqlalchemy.git
   cd Library_project_flask_sqlalchemy
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Project Structure

- `app.py`: Main application file with Flask routes
- `Books.py`: Book model
- `Customers.py`: Customer model
- `Loans.py`: Loan model
- `db.py`: Database configuration
- `unittests.py`: Unit tests for the application

## Running the Application

1. Start the Flask server:
   ```
   python app.py
   ```

2. The server will start running on `http://127.0.0.1:5000/`

## API Endpoints

- `GET /`: Test endpoint
- `GET /search`: Search for books and customers
- `POST /add_customer`: Add a new customer
- `POST /add_book`: Add a new book
- `POST /loan_book`: Create a new loan
- `POST /return_book/<id>`: Return a book
- `GET /books`: Get all books
- `GET /customers`: Get all customers
- `GET /loans`: Get all loans
- `PUT /books/<id>/toggle-status`: Toggle book status
- `PUT /customers/<id>/toggle-status`: Toggle customer status
- `GET /loans/<id>`: Get a specific loan
- `GET /books/<id>`: Get a specific book
- `GET /customers/<id>`: Get a specific customer

## Running Tests

Execute the unit tests by running:
```
python unittests.py
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
