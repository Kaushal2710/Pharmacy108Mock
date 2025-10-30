class Product:
    def __init__(self, name, batch_number, expiry_date, quantity, rate):
        self.name = name
        self.batch_number = batch_number
        self.expiry_date = expiry_date
        self.quantity = quantity
        self.rate = rate

    def calculate_amount(self):
        return self.quantity * self.rate