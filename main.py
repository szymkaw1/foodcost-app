from appGUI import AppGUI
from Product import Ingredient
from Data import Data


product_info = Data()
interface = AppGUI(product_info)

#TODO
# SPRAWDZENIE CZY PRODUKT/SKLADNIK JEST JUZ NA LISCIE
# usuwanie składnikow
# edycja składników
# w tabeli mozna wybrac wartosc procentowa foodcostu, dzieki temu oblicza to nam dla wartosci % dla reszty danych z tabeli (MOZE)
# jak uzytkownik wpisze "," to zamienia na ".",


def check_if_float(field, field_name):

    try:
        converted_value = float(field)
    except ValueError:
        interface.show_wrong_input_warning(field_name)

    else:
        return converted_value


def operate_on_ingredient():
    amount_used = interface.amount_used_entry.get()
    ingredient_price = interface.cost_entry.get()
    product_name = interface.name_entry.get()
    ingredient_name = interface.ingredient_entry.get()
    ingredient_category = interface.ingredient_type.get()

    amount_used = check_if_float(amount_used, "Gramatura / Zużyto sztuk")
    ingredient_price = check_if_float(ingredient_price, "Cena za kilogram / Koszt za paczkę")

    if ingredient_category == "wagowy":
        quantity_in_package = None

        if amount_used is None or ingredient_price is None:
            return

        if amount_used > 0 and ingredient_price > 0:
            ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
                                    ingredient_type=ingredient_category,
                                    quantity_in_package=quantity_in_package)

        else:
            interface.show_must_be_positive_warning()
            return

    if ingredient_category == "sztukowy":
        quantity_in_package = interface.quantity_in_package_entry.get()
        quantity_in_package = check_if_float(quantity_in_package, "Ilość w paczce")

        if amount_used is None or ingredient_price is None or quantity_in_package is None:
            return

        if amount_used > 0 and ingredient_price > 0 and quantity_in_package > 0:
            ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
                                ingredient_type=ingredient_category,
                                quantity_in_package=quantity_in_package)

        else:
            interface.show_must_be_positive_warning()
            return



    interface.show_if_added_info()
    interface.clear_entries()

    product_info.add_data(product_name, ingredient)
    product_info.save_to_json()



def get_table_data():
    interface.clear_table_data(interface.table)
    foodcost_percent_value = interface.get_foodcost_percent_value_from_user()
    product_data = product_info.product_data

    if len(product_data) == 0:
        interface.show_no_data_warning()
    else:
        for product_name in product_data:
            ingredients_total_price = product_info.count_ingredients_price(product_name)
            suggested_price = product_info.count_suggested_price(ingredients_total_price, foodcost_percent_value)

            if foodcost_percent_value is not None:
                interface.insert_to_table(product_name, ingredients_total_price, suggested_price, round(foodcost_percent_value * 100))





interface.add_recipe_button.configure(command=operate_on_ingredient)
interface.load_data_button.configure(command=get_table_data)








interface.root.mainloop()
