class Bill:
    def __init__(self, party_name, party_address):
        self.party_name = party_name
        self.party_address = party_address
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def calculate_total(self):
        total = sum(product.calculate_amount() for product in self.products)
        return total

    def save_bill(self):
        # Logic to save the bill to a database or file can be implemented here
        pass

    def __str__(self):
        bill_details = f"Bill for {self.party_name}, Address: {self.party_address}\n"
        bill_details += "Products:\n"
        for product in self.products:
            bill_details += str(product) + "\n"
        bill_details += f"Total Amount: {self.calculate_total()}"
        return bill_details