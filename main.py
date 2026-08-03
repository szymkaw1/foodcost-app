
from appGUI import AppGUI
from Product import Ingredient
from Data import Data
from Validators import Validator


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
# sprawdzenie czy skladnik znajduje sie obecnie w recepturze


def handle_edit_recipe_name_validation(result_recipe_name_edit, new_name):
    if result_recipe_name_edit is None:
        return False

    if result_recipe_name_edit == "empty":
        interface.show_empty_name_warning("receptury")
        return False

    if result_recipe_name_edit == "too_long":
        interface.show_name_too_long_warning("receptury")
        return False

    if result_recipe_name_edit == "same_name": # same_name - czyli taka sama nazwa jak obecna
        interface.show_name_already_used_warning("receptury")
        return False

    if result_recipe_name_edit == "spaces":
        interface.show_name_has_spaces_warning("receptury")
        return False

    if new_name in product_info.product_data:
        interface.show_name_already_used_warning("receptury")
        return False

    return True


def handle_add_recipe_name_validation(result_recipe_name_add, recipe_name):
    if result_recipe_name_add is None:
        return False

    if result_recipe_name_add == "empty":
        interface.show_empty_name_warning("receptury")
        return False

    if result_recipe_name_add == "too_long":
        interface.show_name_too_long_warning("receptury")
        return False

    if recipe_name in product_info.product_data:
        interface.show_name_already_used_warning("receptury")
        return False

    if result_recipe_name_add == "spaces":
        interface.show_name_has_spaces_warning("receptury")
        return False

    return True

def handle_ingredient_name_validation(result_ingredient_name):
    if result_ingredient_name == "empty":
        interface.show_empty_name_warning("składnika")
        return False

    elif result_ingredient_name == "too_long":
        interface.show_name_too_long_warning("składnika")
        return False

    elif result_ingredient_name == "spaces":
        interface.show_name_has_spaces_warning("składnika")
        return False

    return True


def handle_ingredients_values_validation(validated_ingredient_values):
    if validated_ingredient_values is None:
        interface.show_must_be_num_warning()
        return False


    elif validated_ingredient_values == "non_positive_num":
        interface.show_must_be_positive_warning()
        return False

    return True

def handle_foodcost_value_validation(result_foodcost_value):
    if result_foodcost_value == "cancelled":
        return False

    elif result_foodcost_value == "out_of_range":
        interface.show_out_of_range_warning()
        return False

    return True




def create_ingredient():
    amount_used, ingredient_price, ingredient_name, ingredient_category = interface.get_values_from_entries()

    product_name = interface.selected_product_name

    if product_name is None:
         interface.show_choose_recipe_warning()
         return

    result_ingredient_name = Validator.validate_ingredient_name(ingredient_name)

    if not handle_ingredient_name_validation(result_ingredient_name):
        return

    if ingredient_category == "wagowy":
        quantity_in_package = None

    else:
        quantity_in_package = interface.quantity_in_package_entry.get()

    validated_ingredient_values = Validator.validate_ingredients_values(amount_used, ingredient_price, quantity_in_package)

    if not handle_ingredients_values_validation(validated_ingredient_values):
        return


    amount_used, ingredient_price, quantity_in_package  = validated_ingredient_values # rozpakowanie krotki

    ingredient = Ingredient(name=ingredient_name, unit_price=ingredient_price, amount=amount_used,
                            ingredient_type=ingredient_category,
                            quantity_in_package=quantity_in_package)

    print(product_name)
    return ingredient, product_name


def add_recipe():
    recipe_name = interface.get_recipe_name()
    result_recipe_name = Validator.validate_add_recipe_name(recipe_name)

    if handle_add_recipe_name_validation(result_recipe_name, recipe_name):

        product_info.add_product(recipe_name)
        product_info.save_to_json()
        interface.show_if_added_info("Produkt")
        interface.clear_entries()
        reload_recipe_table()



def add_ingredient():
    created_ingredient = create_ingredient()


    if created_ingredient is None:
        return

    ingredient, product_name = created_ingredient


    if product_name in product_info.product_data:

        if ingredient.name not in product_info.product_data[product_name]:
            product_info.add_ingredient(product_name, ingredient)
            product_info.save_to_json()
            interface.show_if_added_info("Składnik")
            interface.clear_entries()
            reload_recipe_table()
            interface.select_previous_item()
        else:
            interface.show_name_already_used_warning(ingredient.name)


def edit_ingredient():
    old_ingredient_name = interface.edited_ingredient_name

    created_ingredient = create_ingredient()

    if created_ingredient is None:
        return

    ingredient, product_name = created_ingredient

    if (
            ingredient.name == old_ingredient_name or
            ingredient.name not in product_info.product_data[product_name]
    ):
        product_info.edit_ingredient_data(product_name, ingredient, old_ingredient_name)
        product_info.save_to_json()
        interface.show_if_edited_info()
        interface.return_to_disabled_add_recipe_frame()
        reload_recipe_table()


    else:
        interface.show_name_already_used_warning(ingredient.name)
    interface.select_previous_item()


def count_data():
    table_data = []
    product_data = product_info.product_data


    for product_name in product_data:
        ingredients_total_price = product_info.count_ingredients_price(product_name)
        suggested_price = product_info.count_suggested_price(ingredients_total_price, interface.foodcost_value_from_user)


        counted_data = {"product_name": product_name,
                        "ingredients_total_price": ingredients_total_price,
                        "suggested_price": suggested_price,
                        "foodcost_percent_value": interface.foodcost_value_from_user}

        table_data.append(counted_data)


    return table_data


def reload_recipe_table(show_warning=True):
    interface.clear_table_data(interface.table)
    load_recipe_table(show_warning)

    interface.title_ingredients.configure(text="Składniki:")



def load_recipe_table(show_warning=True):
    if not Validator.validate_file_emptiness(product_info.product_data):
        table_data = count_data()
        interface.load_table_data(table_data)
    elif show_warning:
        interface.show_no_data_warning()

def del_ingredient_and_refresh():
    result = interface.get_selected_ingredients()
    if result:
        old_ingredient_name, product_name = result
        product_info.del_ingredient(old_ingredient_name, product_name)
        product_info.save_to_json()
        interface.show_if_deleted_info("Składnik")
        reload_recipe_table()
        interface.select_previous_item()


def del_recipe_and_refresh():
    if Validator.validate_file_emptiness(product_info.product_data):
        interface.title_ingredients.configure(text="Składniki:")
        interface.show_choose_product_warning()
        return

    product_name = interface.get_selected_recipe('usunięcia.')

    if not product_name:
        return

    product_info.del_recipe(product_name)
    product_info.save_to_json()
    interface.show_if_deleted_info("Produkt")

    reload_recipe_table(show_warning=False)


def edit_recipe_name_and_refresh():
    current_name = interface.get_selected_recipe("zmiany nazwy.")

    if not current_name:
        return

    new_name = interface.get_new_recipe_name()

    result_recipe_name_edit = Validator.validate_edit_recipe_name(new_name, current_name)

    if not handle_edit_recipe_name_validation(result_recipe_name_edit, new_name):
        return

    product_info.edit_product_name(current_name, new_name)
    product_info.save_to_json()
    reload_recipe_table()



def change_foodcost_value():
    foodcost_value = interface.get_foodcost_percent_value_from_user()

    result_foodcost_value = Validator.validate_foodcost_value(foodcost_value)

    if not handle_foodcost_value_validation(result_foodcost_value):
        return

    else:
        interface.foodcost_value_from_user = round(foodcost_value / 100, 2)
        reload_recipe_table()
        # interface.select_previous_item()







interface.add_ingredient_button.configure(command=add_ingredient)
interface.save_data_button.configure(command=edit_ingredient)
interface.del_ingredient_button.configure(command=del_ingredient_and_refresh)
interface.del_recipe_button.configure(command=del_recipe_and_refresh)
interface.edit_recipe_name_button.configure(command=edit_recipe_name_and_refresh)
interface.add_recipe_button.configure(command=add_recipe)
interface.add_ingredient_to_recipe_button.configure(command=interface.set_add_ingredient_to_recipe)
interface.change_foodcost_button.configure(command=change_foodcost_value)
reload_recipe_table()

interface.root.mainloop()
