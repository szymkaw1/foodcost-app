import customtkinter as ctk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox



ENTRY_COLOR = "#2E4540"

class AppGUI:
    def __init__(self, recipe_info):
        self.recipe_info = recipe_info
        self.selected_recipe_name = None
        self.edited_ingredient_name = None
        self.foodcost_value_from_user = 0.3
        self.create_window()
        self.create_recipe_frame()
        self.create_recipe_details()
        self.create_save_data_button()
        self.create_return_button()
        self.add_ingredient_button()
        self.create_recipe_table_frame()
        self.create_recipe_table()
        self.create_ingredients_table_frame()
        self.create_ingredients_table()
        self.create_edit_ingredient_button()
        self.create_del_ingredient_button()
        self.create_del_recipe_button()
        self.create_edit_recipe_name_button()
        self.add_recipe_button()
        self.add_ingredient_to_recipe_button()
        self.create_change_foodcost_button()
        self.switch_off_recipe_frame()

    # =================================================== WINDOW ===========================================================

    def create_window(self):
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("Kalkulator Foodcost")
        ctk.set_appearance_mode("dark")

    # =================================================== FRAMES ===========================================================
    def create_recipe_frame(self):
        self.frame_recipe_details = ctk.CTkFrame(self.root, corner_radius=10,
                                                 width=375, height=340, border_width=1, border_color="grey"
                                                 )
        self.frame_recipe_details.grid(column=1, row=0, padx=30, pady=40)
        self.frame_recipe_details.grid_propagate(False) # dzieki temu wielkosc frame jest taka jak ustalono wyzej, nie dostosowuje sie do ilosci widgetow


    def create_recipe_table_frame(self):
        self.recipe_table_frame = ctk.CTkFrame(self.root, corner_radius=10, width=730, height=340, border_color="grey", border_width=1)
        self.recipe_table_frame.grid(row=0, column=2, padx=5, pady=40)
        self.recipe_table_frame.grid_propagate(False)

    def create_ingredients_table_frame(self):
        self.ingredients_table_frame = ctk.CTkFrame(self.root, corner_radius=10, width=730, height=340, border_color="grey", border_width=1)
        self.ingredients_table_frame.grid(row=1,column=2,padx=5,pady=(0,40))
        self.recipe_table_frame.grid_propagate(False)


    # =================================================== CREATE TABLES ===========================================================

    def create_recipe_table(self):
        self.title_recipe = ctk.CTkLabel(self.root, text="Receptury", font=('TkDefaultFont', 15, "bold"))
        self.title_recipe.place(x=470, y=10)

        self.table = ttk.Treeview(self.recipe_table_frame, height=19)
        self.table.grid(column=0, row=0, padx=20, pady=20)

        self.table['columns'] = ("name", "cost", "price", "foodcost")
        self.table["show"] = "headings" # ukrywa pierwsza kolumne, a pokazuje tylko te wymienione wyzej

        self.table.heading("name", text="Nazwa")
        self.table.heading("cost", text="Koszt")
        self.table.heading("price", text="Sugerowana cena")
        self.table.heading("foodcost", text="Foodcost %")

        self.table.column("name", width=262)
        self.table.column("cost", width=262)
        self.table.column("price", width=262)
        self.table.column("foodcost", width=262)



        self.table.bind("<<TreeviewSelect>>", self.load_recipe_ingredients)

    def create_ingredients_table(self):
        self.title_ingredients = ctk.CTkLabel(self.root, text="Składniki:", font=('TkDefaultFont', 15, "bold"))
        self.title_ingredients.place(x=470, y=390)

        self.ingredient_table = ttk.Treeview(self.ingredients_table_frame, height=19)
        self.ingredient_table.grid(column=0, row=0, padx=20, pady=20)
        self.ingredient_table['columns'] = ("name", "amount_used", "unit", "unit_cost", "ingredient_cost")
        self.ingredient_table['show'] = 'headings'

        self.ingredient_table.heading("name", text="Nazwa składnika")
        self.ingredient_table.heading("amount_used", text="Ilość/Zużyto")
        self.ingredient_table.heading("unit", text="Jednostka")
        self.ingredient_table.heading("unit_cost", text="Koszt jednostkowy")
        self.ingredient_table.heading("ingredient_cost", text="Koszt składnika")

        self.ingredient_table.column("name", width=209)
        self.ingredient_table.column("amount_used", width=209)
        self.ingredient_table.column("unit", width=209)
        self.ingredient_table.column("unit_cost", width=209)
        self.ingredient_table.column("ingredient_cost", width=209)



    # ===================================================  TABLE INSERTS ===========================================================

    def insert_to_recipes(self, recipe_name, ingredients_total_price, suggested_price, foodcost_percent_value):

        self.table.insert("", "end",
                                   values=(
                                       recipe_name,
                                       ingredients_total_price,
                                       suggested_price,
                                       foodcost_percent_value
                                   )
                                   )



    def insert_ingredients(self, recipe_name, ingredient_name, amount_used, unit, unit_cost, ingredient_cost):
        self.title_ingredients.configure(text=f"Składniki: {recipe_name}")
        self.ingredient_table.insert("", "end", values=(ingredient_name,
                                                        amount_used,
                                                        unit,
                                                        unit_cost,
                                                        ingredient_cost
                                                        )
                                     )




# =================================================== INGREDIENTS FUNCS ===========================================================
    def get_selected_ingredients(self):
        selected = self.select_data(self.ingredient_table)

        if selected is  None:
            messagebox.showwarning("Oops", "Najpierw wybierz składnik do usunięcia.")
            return False

        values = self.ingredient_table.item(selected[0])
        old_ingredient_name = values['values'][0]
        recipe_name = self.selected_recipe_name

        return old_ingredient_name, recipe_name

    def select_previous_item(self):
        items_id = self.table.get_children()


        selected_recipe_id = None

        for id in items_id:
            values = self.table.item(id)
            selected_recipe = str(values['values'][0])

            if selected_recipe == self.selected_recipe_name:
                selected_recipe_id = id

        if selected_recipe_id is not None:

            self.table.selection_set(selected_recipe_id)

    def get_selected_recipe(self,chosen_task):
        selected = self.select_data(self.table)

        if selected is  None:
            messagebox.showwarning("Oops", f"Najpierw wybierz recepturę do {chosen_task}")
            return False

        values = self.table.item(selected[0])
        selected_recipe = str(values['values'][0])
        self.selected_recipe_name = selected_recipe

        return selected_recipe

    def set_add_ingredient_to_recipe(self):
        self.return_to_disabled_add_recipe_frame()

        self.clear_entries()

        recipe_name = self.get_selected_recipe("dodania składnika.")

        if not recipe_name:
            return

        self.title_add_prod.configure(text=f"Dodaj składnik do: {recipe_name}")
        self.return_button.configure(state='enable')
        self.switch_on_recipe_frame()


    def set_edit_ingredient_panel(self):
        selected = self.select_data(self.ingredient_table)


        if selected is  None:
            messagebox.showwarning("Oops", "Najpierw wybierz składnik do edycji.")
            return

        self.clear_entries()


        values = self.ingredient_table.item(selected[0]) # zwraca słownik
        ingredient_name = str(values['values'][0])

        recipe_name = self.selected_recipe_name
        self.edited_ingredient_name = ingredient_name

        ingredient_values = self.recipe_info.get_ingredient(recipe_name, ingredient_name)
        ingredient_price = ingredient_values['price/kg (price/package)']
        amount_used = ingredient_values['amount']
        quantity_in_package = ingredient_values['quantity']
        recipe_type = ingredient_values["Type"]

        self.title_add_prod.configure(text=f"Edycja składnika: {recipe_name}")
        self.optionmenu.set(recipe_type)
        self.set_ingredient_type(recipe_type)
        self.ingredient_entry.insert(0, ingredient_name)
        self.cost_entry.insert(0, ingredient_price)
        self.amount_used_entry.insert(0, amount_used)

        if recipe_type == "sztukowy":
            self.quantity_in_package_entry.insert(0, quantity_in_package)

        self.switch_to_edit_mode()





    def load_recipe_ingredients(self,event):

        self.clear_table_data(table_name=self.ingredient_table)

        selected = self.select_data(table_name=self.table)

        if selected is None:
            self.title_ingredients.configure(text="Składniki:")
            return

        values = self.table.item(selected[0])
        recipe_name = str(values['values'][0])
        self.selected_recipe_name =  recipe_name
        recipe_data = self.recipe_info.recipe_data

        self.title_ingredients.configure(text=f"Składniki: {recipe_name}")

        for ingredient, values in recipe_data[recipe_name].items():
            ingredient_name = ingredient
            amount_used = values['amount']
            unit_cost = str(values["price/kg (price/package)"])
            ingredient_cost = str(values["price"]) + " zł"
            unit = values["Type"]
            if unit == "sztukowy":
                unit = "szt"
                unit_cost += " zł/paczka"

            else:
                unit = "g"
                unit_cost += " zł/kg"


            self.insert_ingredients(recipe_name, ingredient_name, amount_used, unit, unit_cost, ingredient_cost)


    def set_ingredient_type(self, current_type):

        if current_type == "wagowy":
            self.cost_label.configure(text="Cena za kilogram:")
            self.amount_used_label.configure(text="Gramatura:")
            self.quantity_in_package_entry.configure(state="disabled", fg_color="#495057")
            self.quantity_in_package_label.configure(text_color="#495057")
            self.weight_unit_label.configure(text="g")
            self.weight_unit_label.grid(padx=10)


        else:
            self.cost_label.configure(text="Koszt za całość:")
            self.amount_used_label.configure(text="Zużyto sztuk:")
            self.quantity_in_package_entry.configure(state='normal', fg_color=ENTRY_COLOR)
            self.quantity_in_package_label.configure(text_color="white")
            self.weight_unit_label.configure(text="szt")
            self.weight_unit_label.grid(padx=5)

    # =================================================== ADDING RECIPE CREATION  ===========================================================


    def create_recipe_details(self):
        self.title_add_prod = ctk.CTkLabel(self.root, text="Dodaj składnik do: ", font=('TkDefaultFont', 15, "bold"))
        self.title_add_prod.place(x=60,y=10)


        self.ingredient_type = ctk.StringVar()
        self.option_label = ctk.CTkLabel(self.frame_recipe_details, text="Rodzaj składnika:")
        self.option_label.grid(row=2, column=0, sticky='w', padx=30, pady=10)
        self.optionmenu = ctk.CTkOptionMenu(self.frame_recipe_details, values=["wagowy", "sztukowy"], variable=self.ingredient_type, width=180,
                                            fg_color=ENTRY_COLOR,
                                            command=self.set_ingredient_type)
        self.optionmenu.grid(row=2,column=1,sticky='w')
        self.optionmenu.set("wagowy")


        self.ingredient_label = ctk.CTkLabel(self.frame_recipe_details, text="Nazwa składnika:")
        self.ingredient_label.grid(row=1,column=0, sticky='w', padx=30, pady=15)
        self.ingredient_entry = ctk.CTkEntry(self.frame_recipe_details, width=180, fg_color=ENTRY_COLOR)
        self.ingredient_entry.grid(row=1, column=1, sticky='w')
        self.cost_label = ctk.CTkLabel(self.frame_recipe_details, text="Cena za kilogram:")
        self.cost_label.grid(row=3, column=0, sticky='w', padx=30, pady=15)
        self.cost_entry = ctk.CTkEntry(self.frame_recipe_details, width=150, fg_color=ENTRY_COLOR)
        self.cost_entry.grid(row=3, column=1, sticky='w')
        self.currency_label = ctk.CTkLabel(self.frame_recipe_details, text="zł", anchor='w')
        self.currency_label.grid(row=3,column=1, sticky='e', padx=10)

        self.amount_used_label = ctk.CTkLabel(self.frame_recipe_details, text="Zużyto:")
        self.amount_used_label.grid(row=4, column=0, sticky='w', padx=30, pady=15)
        self.amount_used_entry = ctk.CTkEntry(self.frame_recipe_details, width=150, fg_color=ENTRY_COLOR)
        self.amount_used_entry.grid(row=4, column=1, sticky='w')
        self.weight_unit_label = ctk.CTkLabel(self.frame_recipe_details, text="g", anchor='w')
        self.weight_unit_label.grid(row=4, column=1, sticky='e',padx=10)

        self.quantity_in_package_label = ctk.CTkLabel(self.frame_recipe_details, text="Ilość w paczce:")
        self.quantity_in_package_label.grid(row=5, column=0, sticky='w', padx=30, pady=15)
        self.quantity_in_package_entry = ctk.CTkEntry(self.frame_recipe_details, width=150, fg_color=ENTRY_COLOR)
        self.quantity_in_package_entry.grid(row=5, column=1, sticky='w')
        self.piece_unit_label = ctk.CTkLabel(self.frame_recipe_details, text="szt", anchor='w')
        self.piece_unit_label.grid(row=5, column=1, sticky='e', padx=5)

        self.quantity_in_package_entry.configure(state="disabled", fg_color="#495057")
        self.quantity_in_package_label.configure(text_color="#495057")

    # =================================================== BUTTONS CREATION ===========================================================


    def add_ingredient_button(self):
        self.add_ingredient_button = ctk.CTkButton(self.frame_recipe_details, text="Dodaj składnik", width=150, height=30, fg_color="#467235", corner_radius=5)
        self.add_ingredient_button.grid(row=6, column=1, padx=(0, 30), pady=20, sticky='e')

    def add_recipe_button(self):
        self.add_recipe_button = ctk.CTkButton(self.recipe_table_frame, text="Dodaj recepturę", width=150,
                                               height=30, fg_color="#467235", corner_radius=5)
        self.add_recipe_button.grid(row=1, column=0, padx=(15, 0), pady=(0,15), sticky='w')

    def add_ingredient_to_recipe_button(self):
        self.add_ingredient_to_recipe_button = ctk.CTkButton(self.recipe_table_frame, text="Dodaj składnik do receptury", width=150,
                                                             height=30, fg_color="#467235", corner_radius=5)
        self.add_ingredient_to_recipe_button.grid(row=1, column=0, padx=(175, 0), pady=(0, 15), sticky='w')


    def create_edit_ingredient_button(self):
        self.edit_data_button = ctk.CTkButton(self.ingredients_table_frame, text="Edytuj składnik", width=150, height=30, fg_color="#467235", corner_radius=5, command=self.set_edit_ingredient_panel)
        self.edit_data_button.grid(row=1,column=0, sticky='w', padx=(15,0), pady=(0,15))

    def create_return_button(self):
        self.return_button = ctk.CTkButton(self.frame_recipe_details, state="disabled", text="Powrót", width=150, height=30, fg_color="#467235", corner_radius=5, command=self.return_to_disabled_add_recipe_frame)
        self.return_button.grid(row=6,column=0, sticky='e', padx=(30,5), pady=10)

    def create_save_data_button(self):
        self.save_data_button = ctk.CTkButton(self.frame_recipe_details, text="Zapisz zmiany", width=150, height=30, fg_color="#467235", corner_radius=5)
        self.save_data_button.grid(row=6, column=1, padx=(0, 30), pady=10, sticky='e')
        self.hide_button(self.save_data_button)

    def create_del_ingredient_button(self):
        self.del_ingredient_button = ctk.CTkButton(self.ingredients_table_frame, text="Usuń składnik", width=150,
                                                   height=30, fg_color="#467235", corner_radius=5,
                                                   )
        self.del_ingredient_button.grid(row=1, column=0, sticky='e', padx=(0, 15), pady=(0, 15))


    def create_del_recipe_button(self):
        self.del_recipe_button = ctk.CTkButton(self.recipe_table_frame, text="Usuń recepturę", width=150, height=30, fg_color="#467235", corner_radius=5)
        self.del_recipe_button.grid(row=1,column=0, sticky='e', padx=(0,15), pady=(0,15))

    def create_edit_recipe_name_button(self):
        self.edit_recipe_name_button = ctk.CTkButton(self.recipe_table_frame, text="Zmień nazwę receptury", width=150, height=30,
                                                     fg_color="#467235", corner_radius=5
                                                     )
        self.edit_recipe_name_button.grid(row=1, column=0, sticky='e', padx=(0, 175), pady=(0, 15))

    def create_change_foodcost_button(self):
        self.change_foodcost_button = ctk.CTkButton(self.root, text="Zmiana % foodcost",width=150, height=20,
                                                     fg_color="#34374C", corner_radius=5
                                                     )
        self.change_foodcost_button.place(x=1005, y=15)
    # =================================================== EXTRA FUNCTIONS ===========================================================
    def get_foodcost_percent_value_from_user(self):
        foodcost_value = simpledialog.askinteger(title="Docelowy Food Cost (%)", prompt="Podaj oczekiwany Food Cost (%).")

        return foodcost_value

    def get_new_recipe_name(self):
        new_recipe_name = simpledialog.askstring(title="Nowa nazwa receptury", prompt="Podaj nową nazwę receptury.")
        return new_recipe_name

    def get_recipe_name(self):
        recipe_name = simpledialog.askstring(title="Dodaj nazwę receptury", prompt="Podaj nazwę receptury.")
        return recipe_name
    # =================================================== DIALOGS ===========================================================

    def show_no_data_warning(self):
        messagebox.showwarning(title="Oops", message="Nie mam skąd pobrać danych. Plik jest pusty.")

    def show_wrong_input_warning(self, field_name):
        messagebox.showwarning(title="Oops", message=f"Podano nieprawidłowy typ danych dla '{field_name}'.")

    def show_must_be_positive_warning(self):
        messagebox.showwarning(title="Oops", message="Wartości liczbowe muszą być większe niż 0.")

    def show_if_ingredient_added_info(self):
        messagebox.showinfo(title="Świetnie!", message="Składnik został dodany.")

    def show_if_recipe_added_info(self):
        messagebox.showinfo(title="Świetnie!", message="Receptura została dodana.")


    def show_if_edited_info(self):
        messagebox.showinfo(title="Świetnie!", message="Składnik został zmieniony.")

    def show_if_ingredient_deleted_info(self):
        messagebox.showinfo("Świetnie!", "Składnik został usunięty.")

    def show_if_recipe_deleted_info(self):
        messagebox.showinfo("Świetnie!", "Receptura została usunięta.")

    def show_choose_recipe_del_warning(self):
        messagebox.showwarning("Oops", "Najpierw wybierz recepturę do usunięcia.")

    def show_name_already_used_warning(self, name):
        messagebox.showwarning("Oops", f"Podana nazwa {name} jest już zajęta.")

    def show_empty_name_warning(self, name):
        messagebox.showwarning(title="Oops", message=f"Nazwa {name} nie może być pusta.")

    def show_name_too_long_warning(self, name):
        messagebox.showwarning(title="Oops", message=f"Nazwa {name} jest za długa.")

    def show_name_has_spaces_warning(self, name):
        messagebox.showwarning(title="Oops", message=f"Nazwa {name} niepoprawna. Zwróć uwagę na spacje w nazwie.")


    def show_invalid_number_warning(self):
        messagebox.showwarning(title="Oops", message="Podano niepoprawną wartość liczbową.")

    def show_must_be_num_warning(self):
        messagebox.showwarning(title="Oops", message="Podano nieprawidłową wartość w 'Cena za kilogram' lub 'Zużyto'.")

    def show_empty_foodcost_value_warning(self):
        messagebox.showwarning(title="Oops", message="Pole nie może być puste.")

    def show_out_of_range_warning(self):
        messagebox.showwarning(title="Oops", message="Podana wartość musi należeć do przedziału 1–100.")

    def show_choose_recipe_del_warning(self):
        messagebox.showwarning(title="Oops", message="Nie wybrano receptury.")

    def confirm_user_deletion(self):
        user_answer = messagebox.askyesno(title="Usuwanie", message="Czy jesteś pewien usunięcia?")
        return user_answer
    # =================================================== HELPERS  ===========================================================
    def load_table_data(self, table_data):
        for recipe in table_data:
            recipe_name = recipe["recipe_name"]
            ingredients_total_price = recipe["ingredients_total_price"]
            suggested_price = recipe["suggested_price"]
            foodcost_percent_value = recipe["foodcost_percent_value"]


            self.insert_to_recipes(recipe_name, ingredients_total_price, suggested_price,
                                    round(foodcost_percent_value * 100))



    def clear_table_data(self, table_name):
        table_name.delete(*table_name.get_children()) # * rozpakowuje krotke z get_children(),
        # a get_children zwraca krotke identyfikatorow, czyli produktow z tabeli


    def clear_entries(self):

        self.cost_entry.delete(0, 'end')
        self.amount_used_entry.delete(0, 'end')
        self.ingredient_entry.delete(0, 'end')
        self.quantity_in_package_entry.delete(0, 'end')


    def hide_button(self, button):
        button.grid_forget()


    def show_button(self, button):
        button.grid(row=6, column=1, padx=(0,30), pady=10, sticky="e")


    def select_data(self, table_name):
        selected = table_name.selection()

        if not selected:
            return

        return selected

        # =================================================== GUI MODES  ===========================================================

    def return_to_disabled_add_recipe_frame(self):
        self.clear_entries()
        self.title_add_prod.configure(text="Dodaj składnik do:")
        self.return_button.configure(state='disabled')
        self.hide_button(self.save_data_button)
        self.show_button(self.add_ingredient_button)
        self.switch_off_recipe_frame()


    def switch_off_recipe_frame(self):
        self.option_label.configure(text_color="#495057")
        self.optionmenu.configure(state="disabled", fg_color="#495057")
        self.cost_label.configure(text_color="#495057")
        self.cost_entry.configure(state="disable", fg_color="#495057")
        self.amount_used_label.configure(text_color="#495057")
        self.amount_used_entry.configure(state="disable", fg_color="#495057")
        self.ingredient_label.configure(text_color="#495057")
        self.ingredient_entry.configure(state="disable", fg_color="#495057")

    def switch_on_recipe_frame(self):
        self.option_label.configure(text_color="white")
        self.optionmenu.configure(state='normal', fg_color=ENTRY_COLOR)
        self.cost_label.configure(text_color="white")
        self.cost_entry.configure(state='normal', fg_color=ENTRY_COLOR)
        self.amount_used_label.configure(text_color="white")
        self.amount_used_entry.configure(state='normal', fg_color=ENTRY_COLOR)
        self.ingredient_label.configure(text_color="white")
        self.ingredient_entry.configure(state='normal', fg_color=ENTRY_COLOR)

    def switch_to_edit_mode(self):
        self.title_add_prod.configure(text="Edycja składnika")
        self.switch_on_recipe_frame()
        self.return_button.configure(state='enable')
        self.hide_button(self.add_ingredient_button)
        self.show_button(self.save_data_button)


    def get_values_from_entries(self):
        amount_used = self.amount_used_entry.get()
        ingredient_price = self.cost_entry.get()

        ingredient_name = self.ingredient_entry.get()
        ingredient_category = self.ingredient_type.get()

        return amount_used, ingredient_price, ingredient_name, ingredient_category



