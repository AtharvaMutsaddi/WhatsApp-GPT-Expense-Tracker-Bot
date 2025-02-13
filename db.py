import sqlite3
from datetime import datetime
from typing import List, Tuple, Union
from constants import DB_NAME


def setup_database() -> None:
    """
    Creates the 'expenses' table in the database if it does not already exist.
    This function should be called once before recording expenses.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS expenses (
                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                              amount REAL NOT NULL,
                              currency TEXT DEFAULT 'INR',
                              category TEXT NOT NULL,
                              note TEXT,
                              phone_number TEXT NOT NULL,
                              timestamp TEXT NOT NULL
                              )''')
            conn.commit()
        print("[INFO] Database setup completed successfully.")
    except sqlite3.Error as e:
        print(f"[ERROR] Database setup failed: {e}")

def store_expense(amount: float, category: str, note: str, phone_number: str, currency: str = 'INR') -> str:
    """
    Stores an expense record in the database.

    :param amount: Expense amount.
    :param category: Expense category (e.g., food, transport).
    :param note: Additional notes.
    :param phone_number: User's phone number.
    :param currency: Currency of the expense (default: 'INR').
    :return: Success message.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current timestamp
        
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO expenses (amount, currency, category, note, phone_number, timestamp)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (amount, currency, category, note, phone_number, timestamp),
            )
            conn.commit()
        
        print(f"[INFO] Expense recorded: {amount} {currency} in {category} for {phone_number}")
        return "Expense recorded successfully."
    
    except sqlite3.Error as e:
        print(f"[ERROR] Failed to store expense: {e}")
        return "Failed to record expense. Please try again."

def get_expenses_by_phone(phone_number: str) -> Union[List[Tuple], str]:
    """
    Retrieves all expense records associated with a specific phone number.

    :param phone_number: User's phone number.
    :return: List of expense records or an error message.
    """
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT amount, currency, category, note, timestamp 
                   FROM expenses WHERE phone_number = ?""",
                (phone_number,),
            )
            records = cursor.fetchall()

        if not records:
            return "No expenses found for this phone number."

        print(f"[INFO] Retrieved {len(records)} expenses for {phone_number}")
        return records

    except sqlite3.Error as e:
        print(f"[ERROR] Failed to retrieve expenses: {e}")
        return "Error fetching expenses. Please try again."


