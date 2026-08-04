class Validator:

    @staticmethod
    def validate_spaces_in_text(text):
        return text.startswith(" ") or text.endswith(" ")



    @staticmethod
    def validate_edit_recipe_name(new_name, current_name):
        if new_name is None:
            return None

        if new_name == "":
            return "empty"

        if len(new_name) > 30:
            return "too_long"

        if new_name == current_name:
            return "same_name"

        if Validator.validate_spaces_in_text(new_name):
            return "spaces"

        return "ok"

    @staticmethod
    def validate_add_recipe_name(recipe_name):
        if recipe_name is None:
            return None

        if recipe_name == "":
            return "empty"

        if len(recipe_name) > 30:
            return "too_long"

        if Validator.validate_spaces_in_text(recipe_name):
            return "spaces"

        return "ok"

    @staticmethod
    def validate_float_num(field):

        field = field.replace(",", ".")

        try:
            converted_value = float(field)
        except ValueError:
            return None

        else:
            return converted_value

    @staticmethod
    def validate_ingredients_values(amount_used, ingredient_price, quantity_in_package):

        if quantity_in_package is None:
            amount_used = amount_used.strip()
            ingredient_price = ingredient_price.strip()

            amount_used = Validator.validate_float_num(amount_used)
            ingredient_price = Validator.validate_float_num(ingredient_price)

            if amount_used is None or ingredient_price is None:  # is None, poniewaz w check_if_float() gdy wartosc nie byla liczba, to zwraca None

                return None

            if amount_used > 0 and ingredient_price > 0:
                return amount_used, ingredient_price, quantity_in_package

            else:
                return  "non_positive_num"

        else:
            amount_used = amount_used.strip()
            ingredient_price = ingredient_price.strip()
            quantity_in_package = quantity_in_package.strip()

            quantity_in_package = Validator.validate_float_num(quantity_in_package)
            amount_used = Validator.validate_float_num(amount_used)
            ingredient_price = Validator.validate_float_num(ingredient_price)

            if amount_used is None or ingredient_price is None or quantity_in_package is None:
                return None

            if amount_used > 0 and ingredient_price > 0 and quantity_in_package > 0:
                return amount_used, ingredient_price, quantity_in_package

            else:
                return "non_positive_num"


    @staticmethod
    def validate_ingredient_name(ingredient_name):
        if ingredient_name == "":
            return "empty"

        if len(ingredient_name) > 30:
            return "too_long"

        if Validator.validate_spaces_in_text(ingredient_name):
            return "spaces"

    @staticmethod
    def validate_file_emptiness(dict_to_validate):
        return len(dict_to_validate) == 0


    @staticmethod
    def validate_foodcost_value(foodcost_value):
        if foodcost_value is None:
            return "cancelled"

        if not 0 < foodcost_value <= 100:
            return "out_of_range"

















