import customtkinter as ctk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from Data import Data


ENTRY_COLOR = "#2E4540"

class AppGUI:
    def __init__(self, product_info):
        self.product_info = product_info
        self.selected_product_name = None
        self.edited_ingredient_name = None
        self.foodcost_value_from_user = None
        self.create_window()
        self.create_product_frame()
        self.create_product_details()
        self.create_save_data_button()
        self.create_recipe_button()
        self.create_product_table_frame()
        self.create_product_table()
        self.create_load_data_button()
        self.create_ingredients_table_frame()
        self.create_ingredients_table()
        self.create_edit_ingredient_button()
        self.create_return_button()
        self.create_del_button()


    # =================================================== WINDOW ===========================================================

    def create_window(self):
        self.root = ctk.CTk()
        self.root.geometry("1200x800")
        self.root.title("Kalkulator Foodcost")
        ctk.set_appearance_mode("dark")

    # =================================================== FRAMES ===========================================================
    def create_product_frame(self):
        self.frame_product_details = ctk.CTkFrame(self.root, corner_radius=10,
                                                    width=375,height=340,border_width=1,border_color="grey"
                                       )
        self.frame_product_details.grid(column=1,row=0,padx=30,pady=40)
        self.frame_product_details.grid_propagate(False) # dzieki temu wielkosc frame jest taka jak ustalono wyzej, nie dostosowuje sie do ilosci widgetow
        #self.frame_product_details.grid_columnconfigure(0, weight=1) # powieksza kolumne, tak jak columnspan powieksza widget

    def create_product_table_frame(self):
        self.product_table_frame = ctk.CTkFrame(self.root, corner_radius=10, width=730, height=340, border_color="grey", border_width=1)
        self.product_table_frame.grid(row=0, column=2, padx=5,pady=40)
        self.product_table_frame.grid_propagate(False)

    def create_ingredients_table_frame(self):
        self.ingredients_table_frame = ctk.CTkFrame(self.root, corner_radius=10, width=730, height=340, border_color="grey", border_width=1)
        self.ingredients_table_frame.grid(row=1,column=2,padx=5,pady=(0,40))
        self.product_table_frame.grid_propagate(False)

    # =================================================== CREATE TABLES ===========================================================

    def create_product_table(self):
        self.title_recipe = ctk.CTkLabel(self.root, text="Receptury", font=('TkDefaultFont', 15, "bold"))
        self.title_recipe.place(x=470, y=10)

        self.table = ttk.Treeview(self.product_table_frame,height=19)
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

        # self.style = ttk.Style()
        # self.style.theme_use("clam")
        # self.style.configure("Treeview")
        # self.style.configure("Treeview.Heading")

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

        #self.ingredient_table.bind("<<TreeviewSelect>>", self.edit_ingredient)

    # ===================================================  TABLE INSERTS ===========================================================

    def insert_to_recipes(self, product_name, ingredients_total_price, suggested_price, foodcost_percent_value):

        self.table.insert("", "end",
                                   values=(
                                       product_name,
                                       ingredients_total_price,
                                       suggested_price,
                                       foodcost_percent_value
                                   )
                                   )



    def insert_ingredients(self, product_name, ingredient_name, amount_used, unit, unit_cost, ingredient_cost):
        self.title_ingredients.configure(text=f"Składniki: {product_name}")
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
        product_name = self.selected_product_name

        return old_ingredient_name, product_name


    def set_edit_ingredient_panel(self):
        selected = self.select_data(self.ingredient_table)

        if selected is  None:
            messagebox.showwarning("Oops", "Najpierw wybierz składnik do edycji.")
            return

        self.clear_entries()
        self.name_entry.delete(0, "end")

        values = self.ingredient_table.item(selected[0]) # zwraca słownik
        ingredient_name = values['values'][0]
        product_name = self.selected_product_name
        self.edited_ingredient_name = ingredient_name
        ingredient_values = self.product_info.get_ingredient(product_name, ingredient_name)
        ingredient_price = ingredient_values['price/kg (price/package)']
        amount_used = ingredient_values['amount']
        quantity_in_package = ingredient_values['quantity']
        product_type = ingredient_values["Type"]

        self.optionmenu.set(product_type)
        self.set_ingredient_type(product_type)
        self.name_entry.insert(0, product_name)
        self.ingredient_entry.insert(0, ingredient_name)
        self.cost_entry.insert(0, ingredient_price)
        self.amount_used_entry.insert(0, amount_used)

        if product_type == "sztukowy":
            self.quantity_in_package_entry.insert(0, quantity_in_package)

        self.switch_to_edit_mode()


    def load_recipe_ingredients(self,event):

        self.clear_table_data(table_name=self.ingredient_table)

        selected = self.select_data(table_name=self.table)

        if selected is None:
            return

        values = self.table.item(selected[0])
        print(values)

        product_name = values['values'][0]
        self.selected_product_name = product_name
        product_data = self.product_info.product_data

        for ingredient, values in product_data[product_name].items():
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


            self.insert_ingredients(product_name, ingredient_name, amount_used, unit, unit_cost, ingredient_cost)


    def set_ingredient_type(self, current_type):

        if current_type == "wagowy":
            self.cost_label.configure(text="Cena/Kg:")
            self.amount_used_label.configure(text="Gramatura:")
            self.quantity_in_package_entry.configure(state="disabled", fg_color="#495057")
            self.quantity_in_package_label.configure(text_color="#495057")
            self.weight_unit_label.configure(text="g")
            self.weight_unit_label.grid(padx=10)


        else:
            self.cost_label.configure(text="Koszt za paczkę:")
            self.amount_used_label.configure(text="Zużyto sztuk:")
            self.quantity_in_package_entry.configure(state='normal', fg_color=ENTRY_COLOR)
            self.quantity_in_package_label.configure(text_color="white")
            self.weight_unit_label.configure(text="szt")
            self.weight_unit_label.grid(padx=5)

    # =================================================== ADDING PRODUCT CREATION  ===========================================================


    def create_product_details(self):
        self.title_add_prod = ctk.CTkLabel(self.root, text="Dodaj składnik do receptury", font=('TkDefaultFont', 15, "bold"))
        self.title_add_prod.place(x=60,y=10)

        self.name_label = ctk.CTkLabel(self.frame_product_details, text="Nazwa produktu:")
        self.name_label.grid(row=0,column=0,sticky='w',padx=30,pady=10)
        self.name_entry = ctk.CTkEntry(self.frame_product_details, width=180, fg_color=ENTRY_COLOR)
        self.name_entry.grid(row=0,column=1, sticky='w')


        self.ingredient_type = ctk.StringVar()
        self.option_label = ctk.CTkLabel(self.frame_product_details, text="Rodzaj składnika:")
        self.option_label.grid(row=2, column=0, sticky='w', padx=30, pady=10)
        self.optionmenu = ctk.CTkOptionMenu(self.frame_product_details, values=["wagowy", "sztukowy"], variable=self.ingredient_type, width=180,
                                            fg_color=ENTRY_COLOR,
                                            command=self.set_ingredient_type)
        self.optionmenu.grid(row=2,column=1,sticky='w')
        self.optionmenu.set("wagowy")


        self.ingredient_label = ctk.CTkLabel(self.frame_product_details, text="Nazwa składnika:")
        self.ingredient_label.grid(row=1,column=0, sticky='w', padx=30, pady=10)
        self.ingredient_entry = ctk.CTkEntry(self.frame_product_details, width=180, fg_color=ENTRY_COLOR)
        self.ingredient_entry.grid(row=1, column=1, sticky='w')
        self.cost_label = ctk.CTkLabel(self.frame_product_details, text="Cena za kilogram:")
        self.cost_label.grid(row=3, column=0, sticky='w', padx=30, pady=10)
        self.cost_entry = ctk.CTkEntry(self.frame_product_details, width=150, fg_color=ENTRY_COLOR)
        self.cost_entry.grid(row=3, column=1, sticky='w')
        self.currency_label = ctk.CTkLabel(self.frame_product_details, text="zł", anchor='w')
        self.currency_label.grid(row=3,column=1, sticky='e', padx=10)

        self.amount_used_label = ctk.CTkLabel(self.frame_product_details, text="Zużyto:")
        self.amount_used_label.grid(row=4, column=0, sticky='w', padx=30, pady=10)
        self.amount_used_entry = ctk.CTkEntry(self.frame_product_details, width=150, fg_color=ENTRY_COLOR)
        self.amount_used_entry.grid(row=4, column=1, sticky='w')
        self.weight_unit_label = ctk.CTkLabel(self.frame_product_details, text="g", anchor='w')
        self.weight_unit_label.grid(row=4, column=1, sticky='e',padx=10)

        self.quantity_in_package_label = ctk.CTkLabel(self.frame_product_details, text="Ilość w paczce:")
        self.quantity_in_package_label.grid(row=5, column=0, sticky='w', padx=30, pady=10)
        self.quantity_in_package_entry = ctk.CTkEntry(self.frame_product_details, width=150, fg_color=ENTRY_COLOR)
        self.quantity_in_package_entry.grid(row=5, column=1, sticky='w')
        self.piece_unit_label = ctk.CTkLabel(self.frame_product_details, text="szt", anchor='w')
        self.piece_unit_label.grid(row=5, column=1, sticky='e', padx=5)

        self.quantity_in_package_entry.configure(state="disabled", fg_color="#495057")
        self.quantity_in_package_label.configure(text_color="#495057")

    # =================================================== BUTTONS CREATION ===========================================================


    def create_recipe_button(self):
        self.add_recipe_button = ctk.CTkButton(self.frame_product_details, text="Dodaj składnik", width=150,height=30, fg_color="#467235", corner_radius=5)
        self.add_recipe_button.grid(row=6,column=1, padx=(0,30), pady=10, sticky='e')

    def create_load_data_button(self):
        self.load_data_button = ctk.CTkButton(self.product_table_frame, text="Wczytaj dane", width=150,height=30, fg_color="#467235", corner_radius=5)
        self.load_data_button.grid(row=1,column=0, sticky='w', padx=(15,0))

    def create_edit_ingredient_button(self):
        self.edit_data_button = ctk.CTkButton(self.ingredients_table_frame, text="Edytuj składnik", width=150, height=30, fg_color="#467235", corner_radius=5, command=self.set_edit_ingredient_panel)
        self.edit_data_button.grid(row=1,column=0, sticky='w', padx=(15,0), pady=(0,15))

    def create_return_button(self):
        self.return_button = ctk.CTkButton(self.frame_product_details, text="Powrót do dodawania", width=150,height=30, fg_color="#467235", corner_radius=5, command=self.return_to_add_prod)
        self.return_button.grid(row=6,column=0, sticky='e', padx=(30,5), pady=10)

    def create_save_data_button(self):
        self.save_data_button = ctk.CTkButton(self.frame_product_details, text="Zapisz zmiany", width=150, height=30, fg_color="#467235", corner_radius=5)
        self.save_data_button.grid(row=6, column=1, padx=(0, 30), pady=10, sticky='e')
        self.hide_button(self.save_data_button)

    def create_del_button(self):
        self.del_ingredient_button = ctk.CTkButton(self.ingredients_table_frame, text="Usuń składnik", width=150,
                                                   height=30, fg_color="#467235", corner_radius=5,
                                                   command=self.get_selected_ingredients)
        self.del_ingredient_button.grid(row=1, column=0, sticky='e', padx=(0, 15), pady=(0, 15))






    # =================================================== EXTRA FUNCTIONS ===========================================================
    def get_foodcost_percent_value_from_user(self):

        while True:

            if self.foodcost_value_from_user is None:
                foodcost_value = simpledialog.askinteger(title="Docelowy Food Cost (%)", prompt="Podaj oczekiwany Food Cost (%).")



                if foodcost_value == None:
                    break

                elif 0 < foodcost_value <= 100:
                    self.foodcost_value_from_user = round(foodcost_value / 100, 2)
                    return self.foodcost_value_from_user

                else:
                    messagebox.showwarning(title="Oops", message="Liczba musi być z przedziału od 1 do 100.")
            else:
                return self.foodcost_value_from_user


    # =================================================== DIALOGS ===========================================================

    def show_no_data_warning(self):
        messagebox.showwarning(title="Oops", message="Nie mam skąd pobrać danych. Plik jest pusty.")

    def show_wrong_input_warning(self, field_name):
        messagebox.showwarning(title="Oops", message=f"Podano nieprawidłowy typ danych dla '{field_name}'.")

    def show_must_be_positive_warning(self):
        messagebox.showwarning(title="Oops", message="Wartości liczbowe muszą być większe niż 0.")

    def show_if_added_info(self):
        messagebox.showinfo(title="Świetnie!", message="Składnik został dodany.")

    def show_if_edited_info(self):
        messagebox.showinfo(title="Świetnie!", message="Składnik został zmieniony.")

    def show_if_deleted_info(self):
        messagebox.showinfo("Świetnie!", "Składnik został usunięty.")

    # =================================================== HELPERS  ===========================================================



    def load_table_data(self, table_data):
        for product in table_data:
            product_name = product["product_name"]
            ingredients_total_price = product["ingredients_total_price"]
            suggested_price = product["suggested_price"]
            foodcost_percent_value = product["foodcost_percent_value"]


            self.insert_to_recipes(product_name, ingredients_total_price, suggested_price,
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

    def return_to_add_prod(self):
        self.clear_entries()
        self.name_entry.delete(0,'end')
        self.title_add_prod.configure(text="Dodaj składnik do receptury")
        self.return_button.configure(state='disabled')
        self.name_entry.configure(state="normal", fg_color=ENTRY_COLOR)
        self.name_label.configure(text_color="white")
        self.hide_button(self.save_data_button)
        self.show_button(self.add_recipe_button)



    def switch_to_edit_mode(self):
        self.title_add_prod.configure(text="Edycja składnika")
        self.return_button.configure(state='enable')
        self.name_entry.configure(state="disable", fg_color="#495057")
        self.name_label.configure(text_color="#495057")
        self.hide_button(self.add_recipe_button)
        self.show_button(self.save_data_button)


    def get_values_from_entries(self):
        amount_used = self.amount_used_entry.get()
        ingredient_price = self.cost_entry.get()
        product_name = self.name_entry.get()
        ingredient_name = self.ingredient_entry.get()
        ingredient_category = self.ingredient_type.get()

        return amount_used, ingredient_price, product_name, ingredient_name, ingredient_category






