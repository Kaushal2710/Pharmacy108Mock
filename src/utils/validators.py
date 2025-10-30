def is_not_empty(value):
    return bool(value.strip())

def is_valid_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def is_valid_quantity(value):
    return is_valid_number(value) and int(value) > 0

def is_valid_date(date_string):
    from datetime import datetime
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_product_data(name, batch_number, expiry_date, quantity, rate):
    if not is_not_empty(name):
        return "Product name cannot be empty."
    if not is_not_empty(batch_number):
        return "Batch number cannot be empty."
    if not is_valid_date(expiry_date):
        return "Expiry date must be in YYYY-MM-DD format."
    if not is_valid_quantity(quantity):
        return "Quantity must be a positive integer."
    if not is_valid_number(rate):
        return "Rate must be a valid number."
    return None

def validate_bill_data(party_name, party_contact):
    if not is_not_empty(party_name):
        return "Party name cannot be empty."
    if not is_not_empty(party_contact):
        return "Party contact cannot be empty."
    return None