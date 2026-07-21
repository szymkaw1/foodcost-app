from pandas.core.indexers import check_key_length

from appGUI import AppGUI
from Product import Ingredient
from Data import Data


product_info = Data()
interface = AppGUI(product_info)

#TODO
# SPRAWDZENIE CZY PRODUKT/SKLADNIK JEST JUZ NA LISCIE
# w tabeli mozna wybrac wartosc procentowa foodcostu, dzieki temu oblicza to nam dla wartosci % dla reszty danych z tabeli (MOZE)
# jak uzytkownik wpisze "," to zamienia na ".",
#  zmiana nazwy produktu 11.07
#  wybieranie skladnika z listy i dodawanie skladnika do niej
# lista gotowych już składników, które można dodawać bez wpisywania
# Potwierdzenie przed usunieciem
# zmiana wartosci foodcost, w oknie
# wybieranie skladnika w trybie dodawania zeby automatycznie przypisalo nazwe produktu
# lub wybranie tego za pomoca przycisku pod tabela, cos typu "Dodaj skladnik do receptury"


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

def edit_ingredient():
    old_ingredient_name = interface.edited_ingredient_name

    created_ingredient = create_ingredient()

    if created_ingredient is None:
        return

    ingredient, product_name = created_ingredient

    product_info.edit_data(product_name,ingredient,old_ingredient_name)

    interface.show_if_edited_info()



def count_data():
    table_data = []
    product_data = product_info.product_data
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

def check_if_file_empty():
    return len(product_info.product_data) == 0




def reload_recipe_table(show_warning=True):
    interface.clear_table_data(interface.table)
    load_recipe_table(show_warning)
    if check_if_file_empty():
        interface.title_ingredients.configure(text="Składniki:")

def load_recipe_table(show_warning=True):
    if not check_if_file_empty():
        table_data = count_data()
        interface.load_table_data(table_data)
    elif show_warning:

        interface.show_no_data_warning()

def del_ingredient_and_refresh():
    result = interface.get_selected_ingredients()
    if result:
        old_ingredient_name, product_name = result
        product_info.del_ingredient(old_ingredient_name, product_name)
        interface.show_if_deleted_info("Składnik")
        reload_recipe_table()


def del_recipe_and_refresh():
    if check_if_file_empty():
        interface.title_ingredients.configure(text="Składniki:")
        interface.show_choose_product_info()
        return

    product_name = interface.get_selected_recipe()

    if not product_name:
        return

    product_info.del_recipe(product_name)
    interface.show_if_deleted_info("Produkt")

    reload_recipe_table(show_warning=False)








interface.add_recipe_button.configure(command=add_product)
interface.load_data_button.configure(command=reload_recipe_table)
interface.save_data_button.configure(command=edit_ingredient)
interface.del_ingredient_button.configure(command=del_ingredient_and_refresh)
interface.del_recipe_button.configure(command=del_recipe_and_refresh)





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