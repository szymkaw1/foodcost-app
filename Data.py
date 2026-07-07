import json



class Data:
    def __init__(self):
        self.product_data = {}
        self.load_json()

    def add_data(self, product_name, ingredient):
        if product_name not in self.product_data:

            self.product_data.update({product_name: {ingredient.name: {
                                                "amount": ingredient.amount,
                                                "price": ingredient.ingredient_price,
                                                "price/kg (price/package)": ingredient.unit_price,
                                                "Type": ingredient.ingredient_type}}
            })
        else:
            new_ingredient = {ingredient.name: {
                                                "amount": ingredient.amount,
                                                "price": ingredient.ingredient_price,
                                                "price/kg (price/package)": ingredient.unit_price,
                                                "Type": ingredient.ingredient_type}
            }
            self.product_data[product_name].update(new_ingredient)
        self.save_to_json()

    def save_to_json(self):
        with open("product_data.json", "w", encoding="utf-8") as data_file:
            json.dump(self.product_data, data_file, indent=4,  ensure_ascii=False)


    def load_json(self):
        try:
            with open("product_data.json", "r", encoding="utf-8") as data_file:
                self.product_data = json.load(data_file)

        except FileNotFoundError:
            with open("product_data.json", "w", encoding="utf-8") as data_file:
                 json.dump(self.product_data, data_file, indent=4,  ensure_ascii=False)

    def count_ingredients_price(self, product_name):
        total_price = 0
        ingredient = self.product_data[product_name]

# DODAJE CENE SKLADNIKOW DLA JEDNEGO PRODUKTU
        for ingredient_name, details in ingredient.items():
            ingredient_price = details["price"]
            total_price += ingredient_price

        return round(total_price,3)

    def count_suggested_price(self, product_price, foodcost_percent_value):


        try:
            suggested_price = product_price / foodcost_percent_value
        except TypeError:
            return
        else:
            return round(suggested_price,3)












