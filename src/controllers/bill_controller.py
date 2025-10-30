class BillController:
    def __init__(self, bill_model):
        self.bill_model = bill_model

    def add_item(self, product):
        self.bill_model.add_product(product)

    def save_bill(self):
        # Logic to save the bill
        print("Bill saved with the following details:")
        print(self.bill_model)

    def clear_form(self):
        # Logic to clear the form fields
        print("Form cleared.")

    def print_bill_details(self):
        # Logic to print bill details to console
        print("Bill Details:")
        print(self.bill_model)