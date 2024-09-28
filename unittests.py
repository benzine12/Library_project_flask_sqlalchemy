import random
from datetime import datetime, timedelta
from faker import Faker
from app import app  # Replace with your Flask app's filename without .py
from Books import Books
from Customers import Customer
from Loans import Loans
from db import DB

# Initialize Faker for generating fake data
fake = Faker()

# Define loan duration types
loan_types = {
    1: 10,  # Type 1 - 10 days
    2: 5,   # Type 2 - 5 days
    3: 2    # Type 3 - 2 days
}

# Define probabilities
RETURN_DATE_NULL_PROBABILITY = 0.3  # 30% chance Returndate is NULL
LATE_RETURN_PROBABILITY = 0.2       # 20% chance of being late if Returndate is not NULL
INACTIVE_PROBABILITY = 0.1           # 10% chance of being inactive for customers and books

# Define maximum extra days for late returns
MAX_EXTRA_DAYS = 10  # You can adjust this as needed

def clear_data():
    """Deletes all existing data from Loans, Customers, and Books tables."""
    print("Clearing existing data...")
    DB.session.execute(Loans.__table__.delete())
    DB.session.execute(Customer.__table__.delete())
    DB.session.execute(Books.__table__.delete())
    DB.session.commit()
    print("Existing data cleared.")

def populate_books(n=20):
    """Adds n books to the Books table, marking some as inactive."""
    print(f"Adding {n} books...")
    books = []
    for _ in range(n):
        book_type = random.choice(list(loan_types.keys()))
        is_active = False if random.random() < INACTIVE_PROBABILITY else True  # 10% inactive
        book = Books(
            name=fake.sentence(nb_words=3).rstrip('.'),  # Remove trailing period for cleaner names
            author=fake.name(),
            year_published=random.randint(1950, datetime.now().year),
            type=book_type,  # Assign type as 1, 2, or 3
            is_active=is_active
        )
        books.append(book)
    DB.session.bulk_save_objects(books)
    DB.session.commit()
    inactive_books = sum(not book.is_active for book in books)
    print(f"Added {n} books ({inactive_books} inactive).")

def populate_customers(n=20):
    """Adds n customers to the Customers table, marking some as inactive."""
    print(f"Adding {n} customers...")
    customers = []
    for _ in range(n):
        is_active = False if random.random() < INACTIVE_PROBABILITY else True  # 10% inactive
        customer = Customer(
            name=fake.name(),
            city=fake.city(),
            age=random.randint(18, 80),
            email=fake.unique.email(),
            is_active=is_active
        )
        customers.append(customer)
    DB.session.bulk_save_objects(customers)
    DB.session.commit()
    inactive_customers = sum(not customer.is_active for customer in customers)
    print(f"Added {n} customers ({inactive_customers} inactive).")

def populate_loans(n=50):
    """Adds n loans to the Loans table, with some Returndate as NULL and some as late."""
    print(f"Adding {n} loans...")
    # Fetch only active customers and active books
    active_customers = Customer.query.filter_by(is_active=True).all()
    active_books = Books.query.filter_by(is_active=True).all()
    
    if not active_customers:
        print("No active customers available to create loans.")
        return
    
    if not active_books:
        print("No active books available to create loans.")
        return
    
    loans = []
    for _ in range(n):
        customer = random.choice(active_customers)
        book = random.choice(active_books)
        
        loan_date = fake.date_between(start_date='-1y', end_date='today')
        
        # Determine loan duration based on book type
        loan_duration = loan_types.get(book.type, 5)  # Default to 5 days if type is undefined
        
        # Calculate expected return date
        due_date = loan_date + timedelta(days=loan_duration)
        
        # Decide whether to set Returndate or leave it as NULL
        if random.random() < RETURN_DATE_NULL_PROBABILITY:
            return_date = None  # Book not yet returned
        else:
            # Decide if the return is late
            if random.random() < LATE_RETURN_PROBABILITY:
                # Calculate late return by adding extra days
                extra_days = random.randint(1, MAX_EXTRA_DAYS)
                tentative_return_date = due_date + timedelta(days=extra_days)
                # Ensure Returndate does not exceed today's date
                return_date = tentative_return_date if tentative_return_date <= datetime.now().date() else datetime.now().date()
            else:
                # On-time return
                return_date = due_date if due_date <= datetime.now().date() else datetime.now().date()
        
        # Format dates as strings in 'YYYY-MM-DD' format or set to None
        loan = Loans(
            CustID=customer.id,
            BookID=book.id,
            Loandate=loan_date.strftime('%Y-%m-%d'),
            Returndate=return_date.strftime('%Y-%m-%d') if return_date else None
        )
        loans.append(loan)
    
    DB.session.bulk_save_objects(loans)
    DB.session.commit()
    print(f"Added {n} loans.")

if __name__ == "__main__":
    with app.app_context():
        clear_data()            # Clear existing data
        populate_books(50)      # Add 20 books
        populate_customers(50)  # Add 20 customers
        populate_loans(150)      # Add 50 loans
    print("Database population complete.")