import json



class Data:
    def __init__(self):
        self.recipe_data = {}
        self.load_json()


# =================================== JSON ==================================================
    def save_to_json(self):
        with open("recipe_data.json", "w", encoding="utf-8") as data_file:
            json.dump(self.recipe_data, data_file, indent=4, ensure_ascii=False)


    def load_json(self):
        try:
            with open("recipe_data.json", "r", encoding="utf-8") as data_file:
                self.recipe_data = json.load(data_file)

        except FileNotFoundError:
            with open("recipe_data.json", "w", encoding="utf-8") as data_file:
                 json.dump(self.recipe_data, data_file, indent=4, ensure_ascii=False)

        except json.JSONDecodeError:
            self.recipe_data = {}

    # =================================== COUNTING ==================================================

    def count_ingredients_price(self, recipe_name):
        total_price = 0
        ingredient = self.recipe_data[recipe_name]

# DODAJE CENE SKLADNIKOW DLA JEDNEJ RECEPTURY
        for ingredient_name, details in ingredient.items():
            ingredient_price = details["price"]
            total_price += ingredient_price

        return round(total_price,3)

    def count_suggested_price(self, recipe_price, foodcost_percent_value):
        try:
            suggested_price = recipe_price / foodcost_percent_value
        except TypeError:
            return
        else:
            return round(suggested_price,3)

    # =================================== HELPERS ==================================================

    def get_ingredient(self, recipe_name, ingredient_name):
        return self.recipe_data[recipe_name][ingredient_name]

    # =================================== INGREDIENTS FUNCS ==================================================

    def add_ingredient(self, recipe_name, new_ingredient):
        new_ingredient = {new_ingredient.name: {
            "amount": new_ingredient.amount,
            "price": new_ingredient.ingredient_price,
            "price/kg (price/package)": new_ingredient.unit_price,
            "Type": new_ingredient.ingredient_type,
            "quantity": new_ingredient.quantity_in_package}
        }

        self.recipe_data[recipe_name].update(new_ingredient)

    def del_ingredient(self, old_ingredient_name, recipe_name):
        recipe_data = self.recipe_data[recipe_name]

        if old_ingredient_name in recipe_data:
            del recipe_data[old_ingredient_name]




    # =================================== MAIN FUNCS ==================================================

    def add_recipe(self, recipe_name):
        new_recipe = {recipe_name: {}}

        self.recipe_data.update(new_recipe)

    def edit_ingredient_data(self, recipe_name, new_ingredient, old_ingredient_name):
            self.del_ingredient(old_ingredient_name, recipe_name)
            self.add_ingredient(recipe_name, new_ingredient)


    def del_recipe(self, recipe_name):
        self.recipe_data.pop(recipe_name)



    def edit_recipe_name(self, old_recipe_name, new_recipe_name):
        current_recipe = self.recipe_data[old_recipe_name]
        new_recipe_name = ({new_recipe_name: current_recipe})
        self.recipe_data.update(new_recipe_name)
        self.del_recipe(old_recipe_name)










































