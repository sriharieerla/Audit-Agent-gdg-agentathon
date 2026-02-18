import re

def extract_employee(text):
    """
    Extracts employee details.
    Returns a list of dictionaries.
    """
    # Mock data for testing
    return [
        {
            "name": "Jane Doe",
            "bank_account": "1234567890",
            "ifsc": "SBIN0001234",
            "salary": 50000,
            "attendance": 30
        },
        {
            "name": "John Smith",
            "bank_account": "0987654321",
            "ifsc": "HDFC0005678",
            "salary": 52000,
            "attendance": 28
        }
    ]
