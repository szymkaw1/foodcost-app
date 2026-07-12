from appGUI import AppGUI
from Product import Ingredient
from Data import Data


product_info = Data()
interface = AppGUI(product_info)

#TODO
# SPRAWDZENIE CZY PRODUKT/SKLADNIK JEST JUZ NA LISCIE
# usuwanie składnikow
# w tabeli mozna wybrac wartosc procentowa foodcostu, dzieki temu oblicza to nam dla wartosci % dla reszty danych z tabeli (MOZE)
# jak uzytkownik wpisze "," to zamienia na ".",
#  zmiana nazwy produktu 11.07
#  wybieranie skladnika z listy i dodawanie skladnika do niej


def check_if_float(field, field_name):

    try:
        converted_value = float(field)
    except ValueError:
        interface.show_wrong_input_warning(field_name)

    else:
        return converted_value



def check_if_correct_data(amount_used, ingredient_price, quantity_in_package):
    amount_used = check_if_float(amount_used, "Gramatura / Zużyto sztuk")
    ingredient_price = check_if_float(ingredient_price, "Cena za kilogram / Koszt za paczkę")

    if quantity_in_package is None:

        if amount_used is None or ingredient_price is None: # is None, poniewaz w check_if_float() gdy wartosc nie byla liczba, to zwraca None
            return None

        if amount_used > 0 and ingredient_price > 0:
            return amount_used, ingredient_price, quantity_in_package

        else:
            interface.show_must_be_positive_warning()
            return None

    else:
        quantity_in_package = check_if_float(quantity_in_package, "Ilość w paczce")

        if amount_used is None or ingredient_price is None or quantity_in_package is None:
            return None
        if amount_used > 0 and ingredient_price > 0 and quantity_in_package > 0:
            return amount_used, ingredient_price, quantity_in_package

        else:
            interface.show_must_be_positive_warning()
            return None


def create_ingredient():
    amount_used, ingredient_price, product_name, ingredient_name, ingredient_category = interface.get_values_from_entries()

    if ingredient_category == "wagowy":
        quantity_in_package = None

    else:
        quantity_in_package = interface.quantity_in_package_entry.get()

    validated_data = check_if_correct_data(amount_used, ingredient_price, quantity_in_package)

    if validated_data is None:
        return



    amount_used, ingredient_price, quantity_in_package  = validated_data # rozpakowanie krotki

    ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
                            ingredient_type=ingredient_category,
                            quantity_in_package=quantity_in_package)


    return ingredient, product_name

def add_product():
    created_ingredient = create_ingredient()

    if created_ingredient is  None:
        return

    ingredient, product_name = created_ingredient

    product_info.add_data(product_name, ingredient)

    interface.show_if_added_info()
    interface.clear_entries()
    load_table_data()





def edit_ingredient():
    old_ingredient_name = interface.edited_ingredient_name

    created_ingredient = create_ingredient()

    if created_ingredient is None:
        return

    ingredient, product_name = created_ingredient

    product_info.edit_data(product_name,ingredient,old_ingredient_name)

    interface.show_if_edited_info()
    load_table_data()


def count_data():
    table_data = []
    product_data = product_info.product_data
    if len(product_data) == 0:
        interface.show_no_data_warning()

    else:
        foodcost_percent_value = interface.get_foodcost_percent_value_from_user()
        if foodcost_percent_value is not None:
            for product_name in product_data:
                ingredients_total_price = product_info.count_ingredients_price(product_name)
                suggested_price = product_info.count_suggested_price(ingredients_total_price, foodcost_percent_value)


                counted_data = {"product_name": product_name,
                                "ingredients_total_price": ingredients_total_price,
                                "suggested_price": suggested_price,
                                "foodcost_percent_value": foodcost_percent_value}

                table_data.append(counted_data)


    return table_data


def load_table_data():
    interface.clear_table_data(interface.table)
    table_data = count_data()

    for product in table_data:
        product_name = product["product_name"]
        ingredients_total_price = product["ingredients_total_price"]
        suggested_price = product["suggested_price"]
        foodcost_percent_value = product["foodcost_percent_value"]


        interface.insert_to_table(product_name, ingredients_total_price, suggested_price,
                              round(foodcost_percent_value * 100))




# def load_table_data():
#     interface.clear_table_data(interface.table)
#     foodcost_percent_value = interface.get_foodcost_percent_value_from_user()
#     product_data = product_info.product_data
#
#     if len(product_data) == 0:
#         interface.show_no_data_warning()
#     else:
#         for product_name in product_data:
#             ingredients_total_price = product_info.count_ingredients_price(product_name)
#             suggested_price = product_info.count_suggested_price(ingredients_total_price, foodcost_percent_value)
#
#             if foodcost_percent_value is not None:
#                 interface.insert_to_table(product_name, ingredients_total_price, suggested_price, round(foodcost_percent_value * 100))
#
#


interface.add_recipe_button.configure(command=add_product)
interface.load_data_button.configure(command=load_table_data)
interface.save_data_button.configure(command=edit_ingredient)






interface.root.mainloop()









# def operate_on_ingredient():
#
#     amount_used = interface.amount_used_entry.get()
#     ingredient_price = interface.cost_entry.get()
#     product_name = interface.name_entry.get()
#     ingredient_name = interface.ingredient_entry.get()
#     ingredient_category = interface.ingredient_type.get()
#
#     amount_used = check_if_float(amount_used, "Gramatura / Zużyto sztuk")
#     ingredient_price = check_if_float(ingredient_price, "Cena za kilogram / Koszt za paczkę")
#
#     if ingredient_category == "wagowy":
#         quantity_in_package = None
#
#         if amount_used is None or ingredient_price is None:
#             return
#
#         if amount_used > 0 and ingredient_price > 0:
#             ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
#                                     ingredient_type=ingredient_category,
#                                     quantity_in_package=quantity_in_package)
#
#         else:
#             interface.show_must_be_positive_warning()
#             return
#
#     if ingredient_category == "sztukowy":
#         quantity_in_package = interface.quantity_in_package_entry.get()
#         quantity_in_package = check_if_float(quantity_in_package, "Ilość w paczce")
#
#         if amount_used is None or ingredient_price is None or quantity_in_package is None:
#             return
#
#         if amount_used > 0 and ingredient_price > 0 and quantity_in_package > 0:
#             ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
#                                 ingredient_type=ingredient_category,
#                                 quantity_in_package=quantity_in_package)
#
#         else:
#             interface.show_must_be_positive_warning()
#             return
#
#     interface.show_if_added_info()
#     interface.clear_entries()
#
#     product_info.add_data(product_name, ingredient)
#