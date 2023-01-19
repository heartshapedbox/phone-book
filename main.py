from tkinter import *
from threading import Timer
import customtkinter
import sqlite3
import pyglet
import os
os.chdir('C:\\Users\\Dima\\Documents\\GitHub\\phone-book\\')
pyglet.font.add_file('fonts\\Pacifico.ttf')
customtkinter.set_appearance_mode("light")
customtkinter.set_default_color_theme('dark-blue')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.accent_color1 = '#ededed'
        self.accent_color2 = '#3b65ad'
        self.accent_color3 = '#608bd5'
        self.accent_color4 = '#f878b6'
        self.accent_color5 = '#d6478d'
        self.accent_color6 = '#000000'
        self.accent_header_font = ('Pacifico', 22)
        
        self.title('Phone Book')
        self.iconbitmap('assets\\phone-book.ico')
        self['bg'] = self.accent_color1
        x = int(self.winfo_screenwidth() // 2.5)
        y = int(self.winfo_screenheight() * 0.2)
        x, y = str(x), str(y)
        self.geometry(f'400x400+{x}+{y}')
        self.resizable(0, 0)
        self.show_menu()
    
    
    def show_menu(self):
        self.header_frame = Frame(self, background = self.accent_color1)
        self.header_frame.pack(pady = 25)
        self.header_lbl = customtkinter.CTkLabel(self.header_frame, anchor = 'center', text = 'PhoneBook', text_font = self.accent_header_font, text_color = self.accent_color2)
        self.header_lbl.grid(row = 0, column = 0)
        
        self.menu_frame = Frame(self, background = self.accent_color1)
        self.menu_frame.pack(pady = 5)
        self.btn1 = customtkinter.CTkButton(self.menu_frame, text = 'View phone book', cursor = 'hand2', width = 200, command = lambda:self.show_db())
        self.btn2 = customtkinter.CTkButton(self.menu_frame, text = 'Search for surname', cursor = 'hand2', width = 200, command = lambda:self.show_search_for_surname())
        self.btn3 = customtkinter.CTkButton(self.menu_frame, text = 'Add to phone book', cursor = 'hand2', width = 200, command = lambda:self.show_add_number_to_db())
        self.btn4 = customtkinter.CTkButton(self.menu_frame, text = 'Delete from phone book', cursor = 'hand2', width = 200, command = lambda:self.show_remove_number_from_db())
        self.btn5 = customtkinter.CTkButton(self.menu_frame, text = 'Quit', cursor = 'hand2', width = 200, command = lambda:self.quit())
        
        for i in (self.btn1, self.btn2, self.btn3, self.btn4):
            i.configure(
                fg_color = self.accent_color2,
                hover_color = self.accent_color3,
                text_color = self.accent_color1,
                corner_radius = 6
            )
            self.btn_hover(i, self.accent_color2, self.accent_color1)
            i.pack(pady = 2, ipadx = 2, ipady = 5)
            
            
        self.btn5.configure(
            fg_color = self.accent_color5,
            hover_color = self.accent_color4,
            text_color = self.accent_color1,
            corner_radius = 6
        )
        self.btn_hover(self.btn5, self.accent_color5, self.accent_color1)
        self.btn5.pack(pady = 2, ipadx = 2, ipady = 5)
    
    
    def destroy_menu(self):
        for i in (self.header_frame, self.menu_frame):
            i.destroy()
    
    
    def btn_hover(self, btn, colorfgOnHover, colorfgOnLeave):
        btn.bind("<Enter>", func = lambda i: btn.configure(text_color = colorfgOnHover))
        btn.bind("<Leave>", func = lambda i: btn.configure(text_color = colorfgOnLeave)) 
    
    
    def show_back_button(self):
        self.btn_back = customtkinter.CTkButton(self, text = 'Back To Menu', cursor = 'hand2', width = 200, command = lambda:self.back())
        self.btn_back.configure(
            fg_color = self.accent_color2,
            hover_color = self.accent_color3,
            text_color = self.accent_color1,
            corner_radius = 6
        )
        self.btn_hover(self.btn_back, self.accent_color2, self.accent_color1)
        self.btn_back.pack(pady = 2, ipadx = 2, ipady = 5)
    
    
    def show_add_button(self):
        self.btn_add = customtkinter.CTkButton(self, text = 'Add', cursor = 'hand2', width = 200, command = lambda:self.add())
        self.btn_add.configure(
            fg_color = self.accent_color5,
            hover_color = self.accent_color4,
            text_color = self.accent_color1,
            corner_radius = 6
        )
        self.btn_hover(self.btn_add, self.accent_color5, self.accent_color1)
        self.btn_add.pack(pady = 2, ipadx = 2, ipady = 5)
        
        
    def show_search_button(self):
        self.btn_search = customtkinter.CTkButton(self, text = 'Search', cursor = 'hand2', width = 200, command = lambda:self.search())
        self.btn_search.configure(
            fg_color = self.accent_color5,
            hover_color = self.accent_color4,
            text_color = self.accent_color1,
            corner_radius = 6
        )
        self.btn_hover(self.btn_search, self.accent_color5, self.accent_color1)
        self.btn_search.pack(pady = 2, ipadx = 2, ipady = 5)
        
        
    def show_remove_button(self):
        self.btn_remove = customtkinter.CTkButton(self, text = 'Remove', cursor = 'hand2', width = 200, command = lambda:self.remove())
        self.btn_remove.configure(
            fg_color = self.accent_color5,
            hover_color = self.accent_color4,
            text_color = self.accent_color1,
            corner_radius = 6
        )
        self.btn_hover(self.btn_remove, self.accent_color5, self.accent_color1)
        self.btn_remove.pack(pady = 2, ipadx = 2, ipady = 5)
    
    
    def show_db(self):
        self.destroy_menu()
        self.page_name = 'show_db_frame'
        self.db_frame = Frame(self, background = self.accent_color1)
        self.db_frame.pack(pady = 30)
        self.label = customtkinter.CTkLabel(self.db_frame, text = '')
        tmp = []
        db = sqlite3.connect('database\\phone-book.db')
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Names""")
        
        for i in cursor.fetchall():
            tmp.append(f'{i[0]}:   {i[1]} {i[2]},   Phone Number:   {i[3]}')
            
        self.label.configure(
            text = '\n'.join(str(i) for i in tmp),
            justify = LEFT,
            bg_color = self.accent_color1
            )
        self.label.pack()
        self.show_back_button()
        
    
    def show_add_number_to_db(self):
        self.destroy_menu()
        self.page_name = 'show_add_number_frame'
        self.new_number_frame = Frame(self, background = self.accent_color1)
        self.new_number_frame.pack(pady = 30)
        
        self.name_label = customtkinter.CTkLabel(self.new_number_frame, anchor = 'e', text = 'Enter a name:   ')
        self.name_label.grid(row = 0, column = 0, pady = 2)
        self.surname_label = customtkinter.CTkLabel(self.new_number_frame, anchor = 'e', text = 'Enter a surname:   ')
        self.surname_label.grid(row = 1, column = 0, pady = 2)
        self.number_label = customtkinter.CTkLabel(self.new_number_frame, anchor = 'e', text = 'Enter a phone number:   ')
        self.number_label.grid(row = 2, column = 0, pady = 2)
        
        self.name_entry = customtkinter.CTkEntry(self.new_number_frame, border_width = 0, corner_radius = 6)
        self.name_entry.after(500, lambda: self.name_entry.focus())
        self.name_entry.grid(row = 0, column = 1)
        self.surname_entry = customtkinter.CTkEntry(self.new_number_frame, border_width = 0, corner_radius = 6)
        self.surname_entry.grid(row = 1, column = 1)
        self.number_entry = customtkinter.CTkEntry(self.new_number_frame, border_width = 0, corner_radius = 6)
        self.number_entry.grid(row = 2, column = 1)
        
        self.message = customtkinter.CTkLabel(self.new_number_frame, anchor = 's', text = '')
        self.message.grid(row = 4, columnspan = 2, ipady = 10)
        self.show_add_button()
        self.show_back_button()
        
        
    def show_search_for_surname(self):
        self.destroy_menu()
        self.page_name = 'show_search_for_surname_frame'
        self.search_for_surname_frame = Frame(self, background = self.accent_color1)
        self.search_for_surname_frame.pack(pady = 30)
        
        self.search_for_surname = customtkinter.CTkLabel(self.search_for_surname_frame, anchor = 'e', text = 'Enter a surname:   ')
        self.search_for_surname.grid(row = 0, column = 0, pady = 2)
        
        self.search_for_surname_entry = customtkinter.CTkEntry(self.search_for_surname_frame, border_width = 0, corner_radius = 6)
        self.search_for_surname_entry.after(500, lambda: self.search_for_surname_entry.focus())
        self.search_for_surname_entry.grid(row = 0, column = 1)
        
        self.message = customtkinter.CTkLabel(self.search_for_surname_frame, anchor = 's', text = '')
        self.message.grid(row = 4, columnspan = 2, ipady = 10)
        self.show_search_button()
        self.show_back_button()
        
        
    def show_remove_number_from_db(self):
        self.destroy_menu()
        self.page_name = 'show_remove_number_from_db'
        self.remove_number_from_db_frame = Frame(self, background = self.accent_color1)
        self.remove_number_from_db_frame.pack(pady = 30)
        
        self.search_for_id = customtkinter.CTkLabel(self.remove_number_from_db_frame, anchor = 'e', text = 'Enter an ID:   ')
        self.search_for_id.grid(row = 0, column = 0, pady = 2)
        
        self.search_for_id_entry = customtkinter.CTkEntry(self.remove_number_from_db_frame, border_width = 0, corner_radius = 6)
        self.search_for_id_entry.after(500, lambda: self.search_for_id_entry.focus())
        self.search_for_id_entry.grid(row = 0, column = 1)
        
        self.message = customtkinter.CTkLabel(self.remove_number_from_db_frame, anchor = 's', text = '')
        self.message.grid(row = 4, columnspan = 2, ipady = 10)
        self.show_remove_button()
        self.show_back_button()
    
    
    def add(self):
        self.name = self.name_entry.get()
        self.surname = self.surname_entry.get()
        self.number = self.number_entry.get()
        db = sqlite3.connect('database\\phone-book.db')
        cursor = db.cursor()
        
        if len(self.name) > 0 and len(self.surname) > 0 and len(self.number) > 0:
            cursor.execute("""INSERT INTO Names(FirstName, Surname, PhoneNumber) VALUES(?,?,?)""", (self.name, self.surname, self.number))
            db.commit()
            self.message.configure(text = 'Added!', text_color = self.accent_color2)
            Timer(1.5, self.remove_message).start()
        else:
            self.message.configure(text = 'Please, fill all the fields!', text_color = self.accent_color5)
            Timer(1.5, self.remove_message).start()
            
        db.close()
        self.name_entry.delete(0, END)
        self.surname_entry.delete(0, END)
        self.number_entry.delete(0, END)
        
        
    def search(self):
        self.surname = self.search_for_surname_entry.get()
        tmp = []
        db = sqlite3.connect('database\\phone-book.db')
        cursor = db.cursor()
        
        if len(self.surname) > 0:
            cursor.execute(f"""SELECT * FROM Names WHERE Surname = '{self.surname}' """)
            
            for i in cursor.fetchall():
                tmp.append(f'{i[1]} {i[2]},   Phone Number:   {i[3]}')
                db.commit()
                
            if len(tmp) > 0:
                self.message.configure(text = '\n'.join(str(i) for i in tmp), text_color = self.accent_color6, justify = LEFT)
            else:
                self.message.configure(text = 'No matches.', text_color = self.accent_color5, justify = LEFT)
                Timer(1.5, self.remove_message).start()
        else:
            self.message.configure(text = 'Please, fill the field!', text_color = self.accent_color5)
            Timer(1.5, self.remove_message).start()
            
        db.close()
        self.search_for_surname_entry.delete(0, END)
        
    
    def remove(self):
        self.id = self.search_for_id_entry.get()
        tmp = []
        db = sqlite3.connect('database\\phone-book.db')
        cursor = db.cursor()
        cursor.execute("""SELECT * FROM Names""")
        
        for i in cursor.fetchall():
            tmp.append(f'{i[0]}')
            
        if self.id in tmp:
            cursor.execute(f"""DELETE FROM Names WHERE ID = '{self.id}' """)
            db.commit()
            self.message.configure(text = 'Removed!', text_color = self.accent_color2, justify = LEFT)
            Timer(1.5, self.remove_message).start()
        else:
            self.message.configure(text = 'No matches.', text_color = self.accent_color5, justify = LEFT)
            Timer(1.5, self.remove_message).start()
            
        db.close()
        self.search_for_id_entry.delete(0, END)
    
    
    def remove_message(self):
        self.message.configure(text = '')
    
    
    def back(self):
        if self.page_name == 'show_db_frame':
            self.db_frame.destroy()
        elif self.page_name == 'show_add_number_frame':
            self.new_number_frame.destroy()
            self.btn_add.destroy()
        elif self.page_name == 'show_search_for_surname_frame':
            self.search_for_surname_frame.destroy()
            self.btn_search.destroy()
        else:
            self.remove_number_from_db_frame.destroy()
            self.btn_remove.destroy()
        self.btn_back.destroy()
        self.show_menu()
    
    
    def quit(self):
        self.destroy()


if __name__ == "__main__":
    App().mainloop()