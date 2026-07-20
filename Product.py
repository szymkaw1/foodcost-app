class Ingredient:
    def __init__(self, name, unit_price, amount, ingredient_type, quantity_in_package):
        self.name = str(name)
        self.unit_price = unit_price
        self.amount = amount
        self.ingredient_type = ingredient_type
        self.quantity_in_package = quantity_in_package
        self.ingredient_price = 0
        self.calculate_ingredients_price()


    def calculate_ingredients_price(self):
        if self.ingredient_type == "wagowy":
            price_per_kg = float(self.unit_price)
            grams = float(self.amount)
            self.ingredient_price = round((price_per_kg * grams), 2) / 1000

        if self.ingredient_type == "sztukowy":
            price_per_package = float(self.unit_price)
            quantity_used = float(self.amount)
            package_quantity = float(self.quantity_in_package)
            price_per_piece = price_per_package/package_quantity
            self.ingredient_price = round(price_per_piece * quantity_used, 2)






