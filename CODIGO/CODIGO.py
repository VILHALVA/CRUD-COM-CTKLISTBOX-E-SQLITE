import sqlite3
import os
import customtkinter as ctk
from CTkListbox import *

def get_db_path():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, 'items.db')
    return db_path

def connect_db():
    conn = sqlite3.connect(get_db_path())
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL
                      )''')
    conn.commit()
    conn.close()

def add_item(name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name) VALUES (?)", (name,))
    conn.commit()
    conn.close()

def update_item(item_id, name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ? WHERE id = ?", (name, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_all_items():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

class ListboxDemo(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CRUD COM CTKLISTBOX E SQLITE")
        self.geometry("400x400")
        
        create_table()  

        self.init_components()

    def init_components(self):
        self.listbox = CTkListbox(self, command=self.show_selected_item)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.refresh_listbox()

        self.lbl_name = ctk.CTkLabel(self, text="NOME:")
        self.lbl_name.pack(pady=5)

        self.txt_name = ctk.CTkEntry(self)
        self.txt_name.pack(pady=5)

        self.btn_add = ctk.CTkButton(self, text="ADICIONAR", command=self.add_item_to_db)
        self.btn_add.pack(pady=5)

        self.btn_update = ctk.CTkButton(self, text="ATUALIZAR", command=self.update_item_in_db)
        self.btn_update.pack(pady=5)

        self.btn_delete = ctk.CTkButton(self, text="APAGAR", command=self.delete_item_from_db)
        self.btn_delete.pack(pady=5)

        self.btn_clear = ctk.CTkButton(self, text="LIMPAR", command=self.clear_fields)
        self.btn_clear.pack(pady=5)

        self.btn_refresh = ctk.CTkButton(self, text="UPGRADE", command=self.refresh_listbox)
        self.btn_refresh.pack(pady=5)

    def show_selected_item(self, selected_option):
        self.txt_name.delete(0, 'end')
        self.txt_name.insert(0, selected_option)
        self.lbl_name.configure(text=f"NOME: {selected_option}")

    def add_item_to_db(self):
        name = self.txt_name.get()
        if name:
            add_item(name)
            self.refresh_listbox()
            self.clear_fields()
        else:
            self.show_warning("Por favor, insira um nome para adicionar.")

    def update_item_in_db(self):
        selected_index = self.listbox.curselection()
        if isinstance(selected_index, int) and selected_index >= 0:
            item_id = selected_index + 1  
            name = self.txt_name.get()
            if name:
                update_item(item_id, name)
                self.refresh_listbox()
                self.clear_fields()
            else:
                self.show_warning("Por favor, insira um nome para atualizar.")
        else:
            self.show_warning("Selecione um item para atualizar.")

    def delete_item_from_db(self):
        selected_index = self.listbox.curselection()
        if isinstance(selected_index, int) and selected_index >= 0:
            item_id = selected_index + 1  
            delete_item(item_id)
            self.refresh_listbox()
            self.clear_fields()
        else:
            self.show_warning("Selecione um item para deletar.")

    def refresh_listbox(self):
        self.listbox.delete(0, 'end')
        items = get_all_items()
        for item in items:
            self.listbox.insert('end', item[1])  

    def clear_fields(self):
        self.txt_name.delete(0, 'end')
        self.lbl_name.configure(text="Nome:")

    def show_warning(self, message):
        top = ctk.CTkToplevel(self)
        top.geometry("300x100")
        top.title("Aviso")
        
        lbl_message = ctk.CTkLabel(top, text=message)
        lbl_message.pack(pady=20)

        btn_ok = ctk.CTkButton(top, text="OK", command=top.destroy)
        btn_ok.pack()

if __name__ == "__main__":
    app = ListboxDemo()
    app.mainloop()
