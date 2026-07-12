import json



class Data:
    def __init__(self):
        self.product_data = {}
        self.load_json()


# =================================== JSON ==================================================
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

    # =================================== COUNTING ==================================================

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

    # =================================== HELPERS ==================================================

    def get_ingredient(self, product_name, ingredient_name):
        return self.product_data[product_name][ingredient_name]

    # =================================== INGREDIENTS FUNCS ==================================================

    def add_ingredient(self, product_name, new_ingredient):
        new_ingredient = {new_ingredient.name: {
            "amount": new_ingredient.amount,
            "price": new_ingredient.ingredient_price,
            "price/kg (price/package)": new_ingredient.unit_price,
            "Type": new_ingredient.ingredient_type,
            "quantity": new_ingredient.quantity_in_package}
        }

        self.product_data[product_name].update(new_ingredient)

    def del_ingredient(self, old_ingredient_name, product_name):
        product_data = self.product_data[product_name]

        if old_ingredient_name in product_data:
            del product_data[old_ingredient_name]


    # =================================== MAIN FUNCS ==================================================

    def add_product(self, product_name, ingredient):
        new_product = ({product_name: {ingredient.name: {
            "amount": ingredient.amount,
            "price": ingredient.ingredient_price,
            "price/kg (price/package)": ingredient.unit_price,
            "Type": ingredient.ingredient_type,
            "quantity": ingredient.quantity_in_package}}
        })

        self.product_data.update(new_product)

    def edit_data(self, product_name, new_ingredient, old_ingredient_name):
        if product_name in self.product_data:
            self.del_ingredient(old_ingredient_name, product_name)
            self.add_ingredient(product_name, new_ingredient)

        self.save_to_json()

    def add_data(self, product_name, ingredient):
        if product_name not in self.product_data:
            self.add_product(product_name, ingredient)

        else:
            self.add_ingredient(product_name, ingredient)

        self.save_to_json()




























