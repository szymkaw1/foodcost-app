
from appGUI import AppGUI
from Product import Ingredient
from Data import Data
from Validators import Validator


recipe_info = Data()
interface = AppGUI(recipe_info)

#TODO
# lista gotowych już składników, które można dodawać bez wpisywania



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

    if new_name in recipe_info.recipe_data:
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

    if recipe_name in recipe_info.recipe_data:
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

    recipe_name = interface.selected_recipe_name

    if recipe_name is None:
         interface.show_choose_recipe_del_warning()
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


    return ingredient, recipe_name


def add_recipe():
    recipe_name = interface.get_recipe_name()
    result_recipe_name = Validator.validate_add_recipe_name(recipe_name)

    if handle_add_recipe_name_validation(result_recipe_name, recipe_name):

        recipe_info.add_recipe(recipe_name)
        recipe_info.save_to_json()
        interface.show_if_recipe_added_info()
        interface.clear_entries()
        reload_recipe_table()



def add_ingredient():
    created_ingredient = create_ingredient()


    if created_ingredient is None:
        return

    ingredient, recipe_name = created_ingredient


    if recipe_name in recipe_info.recipe_data:

        if ingredient.name not in recipe_info.recipe_data[recipe_name]:
            recipe_info.add_ingredient(recipe_name, ingredient)
            recipe_info.save_to_json()
            interface.show_if_ingredient_added_info()
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

    ingredient, recipe_name = created_ingredient

    if (
            ingredient.name == old_ingredient_name or
            ingredient.name not in recipe_info.recipe_data[recipe_name]
    ):
        recipe_info.edit_ingredient_data(recipe_name, ingredient, old_ingredient_name)
        recipe_info.save_to_json()
        interface.show_if_edited_info()
        interface.return_to_disabled_add_recipe_frame()
        reload_recipe_table()


    else:
        interface.show_name_already_used_warning(ingredient.name)
    interface.select_previous_item()


def count_data():
    table_data = []
    recipe_data = recipe_info.recipe_data


    for recipe_name in recipe_data:
        ingredients_total_price = recipe_info.count_ingredients_price(recipe_name)
        suggested_price = recipe_info.count_suggested_price(ingredients_total_price, interface.foodcost_value_from_user)


        counted_data = {"recipe_name": recipe_name,
                        "ingredients_total_price": ingredients_total_price,
                        "suggested_price": suggested_price,
                        "foodcost_percent_value": interface.foodcost_value_from_user}

        table_data.append(counted_data)


    return table_data


def reload_recipe_table():
    interface.clear_table_data(interface.table)
    load_recipe_table()

    interface.title_ingredients.configure(text="Składniki:")



def load_recipe_table():
    if not Validator.validate_file_emptiness(recipe_info.recipe_data):
        table_data = count_data()
        interface.load_table_data(table_data)


def del_ingredient_and_refresh():

    result = interface.get_selected_ingredients()
    if result:
        user_answer = interface.confirm_user_deletion()

        if user_answer:
            old_ingredient_name, recipe_name = result
            recipe_info.del_ingredient(old_ingredient_name, recipe_name)
            recipe_info.save_to_json()
            interface.show_if_ingredient_deleted_info()
            reload_recipe_table()
            interface.select_previous_item()


def del_recipe_and_refresh():

    if Validator.validate_file_emptiness(recipe_info.recipe_data):
        interface.title_ingredients.configure(text="Składniki:")
        interface.show_choose_recipe_warning()
        return


    recipe_name = interface.get_selected_recipe('usunięcia.')

    if not recipe_name:
        return

    user_answer = interface.confirm_user_deletion()

    if user_answer:

        recipe_info.del_recipe(recipe_name)
        recipe_info.save_to_json()
        interface.show_if_recipe_deleted_info()

        reload_recipe_table()


def edit_recipe_name_and_refresh():
    current_name = interface.get_selected_recipe("zmiany nazwy.")

    if not current_name:
        return

    new_name = interface.get_new_recipe_name()

    result_recipe_name_edit = Validator.validate_edit_recipe_name(new_name, current_name)

    if not handle_edit_recipe_name_validation(result_recipe_name_edit, new_name):
        return

    recipe_info.edit_recipe_name(current_name, new_name)
    recipe_info.save_to_json()
    reload_recipe_table()



def change_foodcost_value():
    foodcost_value = interface.get_foodcost_percent_value_from_user()

    result_foodcost_value = Validator.validate_foodcost_value(foodcost_value)

    if not handle_foodcost_value_validation(result_foodcost_value):
        return

    else:
        interface.foodcost_value_from_user = round(foodcost_value / 100, 2)
        reload_recipe_table()








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
