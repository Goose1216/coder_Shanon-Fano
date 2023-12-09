import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox as mb
import os

class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack()

        self.frm = tk.Frame()
        self.frm.pack(anchor='nw')

        self.browse_button = tk.Button(self.frm, text="Выбор файла", command=self.browse_file, bd=5)
        self.browse_button.pack(side='left', padx=3)

        self.encode_button = tk.Button(self.frm, text='Кодирование текста', command=self.encode, bd=5)
        self.encode_button.pack(side='left', padx=3)

        self.decode_button = tk.Button(self.frm, text='Декодирование текста', command=self.encode, bd=5)
        self.decode_button.pack(side='left', padx=3)

        self.save_button = tk.Button(self.frm, text='Сохранить результат', command=self.save_data, bd=5)
        self.save_button.pack(side='left', padx=3)

        font1 = font.Font(family="Ubuntu Mono", size=10)
        self.text_field = tk.Text(master, bd=5, font=font1, wrap="word")
        self.text_field.pack(anchor='w')
        self.text_field.insert(0.0, 'There is no text')
        self.text_field.config(state='disabled')

        font1 = font.Font(family="Ubuntu Mono", size=10)
        self.text_field_new = tk.Text(master, bd=5, font=font1, wrap="word")
        self.text_field_new.pack(anchor='w')
        self.text_field_new.config(state='disabled')

    def browse_file(self, ):
        file_dir = filedialog.askopenfilename(title="Выбор файла", initialdir=os.path.curdir, defaultextension='txt',  filetypes=(("TXT files", "*.txt"),
                                                                                                                                  ("All files", "*.*"),))
        try:
            with open(file_dir, encoding='utf-8') as f:
                try:
                    text = f.read()
                    self.text_field.config(state='normal')
                    self.text_field.delete(0.0, 'end')
                    self.text_field.insert(0.0, text)
                    self.text_field.config(state='disabled')
                except UnicodeDecodeError:
                    mb.showwarning("ERROR", message='Не поддерживаемый тип файла или в нём кодировка не utf-8')
        except FileNotFoundError:
            if file_dir != '':
                mb.showwarning("ERROR", message=f'Не найдена директория {file_dir}')


    def encode(self):
        pass

    def decode(self):
        pass

    def save_data(self):
        pass

root = tk.Tk()
root.title("Архиватор")
root.minsize(525, 400)
root.geometry('600x800')
root.iconphoto(False, tk.PhotoImage(file="icon.png"))

myapp = App(root)
myapp.mainloop()