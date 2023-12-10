import tkinter as tk
from tkinter import font
from tkinter import filedialog
from tkinter import messagebox as mb
import os


class App(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.alph = None
        self.need_alph = False
        self.pack()

        self.frm = tk.Frame()
        self.frm.pack(anchor='nw')

        self.browse_button = tk.Button(self.frm, text="Выбор файла", command=self.browse_file, bd=5)
        self.browse_button.pack(side='left', padx=3)

        self.encode_button = tk.Button(self.frm, text='Кодирование текста', command=self.encode, bd=5)
        self.encode_button.pack(side='left', padx=3)

        self.decode_button = tk.Button(self.frm, text='Декодирование текста', command=self.decode, bd=5)
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

        self.text = 'There is no text'
        self.text_new = ''

    def browse_file(self, ):
        try:
            file_dir = filedialog.askopenfilename(title="Выбор файла",
                                                  initialdir=os.path.curdir,
                                                  defaultextension='txt',
                                                  filetypes=(("TXT files", "*.txt"),
                                                             ("All files", "*.*"),))
            codecs = ['utf-8', 'ascii', 'cp1251']
            for codec in codecs:
                try:
                    f = open(file_dir, encoding=codec)
                    self.text_field.config(state='normal')
                    self.text_field.delete(0.0, 'end')
                    self.text = f.read()
                    if len(self.text) > 5000:
                        self.text_field.insert(0.0, self.text[:5000] + '...')
                    else:
                        self.text_field.insert(0.0, self.text)
                    self.text_field.config(state='disabled')
                    f.close()
                    break
                except UnicodeDecodeError as e:
                    if codec == codecs[-1]:
                        mb.showwarning("ERROR", message='Не поддерживаемый тип файла или в нём кодировка не utf-8')
                        print(e)
                    else:
                        continue
        except FileNotFoundError as e:
            if file_dir != '':
                mb.showwarning("ERROR", message=f'Не найдена директория {file_dir}')
            print(e)

    def encode(self):
        self.alph = {}
        self.need_alph = True

        def create_code(sequence, num=None):
            if num is not None:
                for letter in sequence:
                    if letter in self.alph:
                        self.alph[letter] += num
                    else:
                        self.alph[letter] = num
            index = 1
            sum_left = round(probability[0][1], 10)
            sum_right = round((sum((x[1] for x in probability[1: len(sequence)]))), 10)
            if sum_left < sum_right:
                while sum_right > sum_left and index < len(sequence):
                    sum_left = round(sum_left + probability[index][1], 10)
                    sum_right = round(sum_right - probability[index][1], 10)
                    index += 1
                    if sum_left > sum_right:
                        index -= 1
                        sum_left = round(sum_left - probability[index][1], 10)
                        sum_right = round(sum_right + probability[index][1], 10)
                        break
            sequence1 = sequence[0: index]
            sequence2 = sequence[index: len(sequence)]
            if len(sequence1) > 1:
                create_code(sequence1, '1')
            else:
                if sequence1[0] in self.alph:
                    self.alph[sequence1[0]] += '1'
                else:
                    self.alph[sequence1[0]] = '1'
            if len(sequence2) > 1:
                create_code(sequence2, '0')
            else:
                if sequence2[0] in self.alph:
                    self.alph[sequence2[0]] += '0'
                else:
                    self.alph[sequence2[0]] = '0'

        probability = self.generate_probabilities()
        seq = [word[0] for word in probability]
        create_code(seq)
        self.text_field_new.config(state='normal')
        self.text_field_new.delete(0.0, 'end')
        self.text_new = ''
        for w in self.text:
            self.text_new += self.alph[w]
        if len(self.text_new) > 5000:
            self.text_field_new.insert(0.0, self.text_new[:5000] + '...')
        else:
            self.text_field_new.insert(0.0, self.text_new)
        self.text_field_new.config(state='disabled')

    def decode(self):
        text = self.text
        self.need_alph = False
        text_decode = ''
        seq = ''
        end_of_alph = text.find('}')
        alph = {k[1:-1]: v[1:-1] for v, k in [s.split(': ') for s in text[1:end_of_alph].split(', ')]}
        print(alph)
        text = text[end_of_alph+2:]
        print(text)
        for w in text:
            seq += w
            if seq in alph:
                word = alph[seq] if alph[seq] != '\\n' else '\n'
                text_decode += word
                seq = ''
        print(text_decode)
        self.text_field_new.config(state='normal')
        self.text_field_new.delete(0.0, 'end')
        self.text_new = text_decode
        if len(self.text_new) > 5000:
            self.text_field_new.insert(0.0, self.text_new[:5000] + '...')
        else:
            self.text_field_new.insert(0.0, self.text_new)
        self.text_field_new.config(state='disabled')

    def save_data(self,):
        f = filedialog.asksaveasfile(mode='w',
                                     initialfile='Decode.txt',
                                     title="Cохранение файла",
                                     initialdir=os.path.curdir,
                                     defaultextension='.txt',
                                     filetypes=(("TXT files", "*.txt"), ("All files", "*.*"), ))
        if f is None:
            return
        text_for_save = str(self.alph) + '\n' + self.text_new if self.need_alph else self.text_new
        f.write(text_for_save)
        f.close()

    def generate_probabilities(self):
        text = self.text
        len_text = len(text)
        probability = []
        alph = {}
        for w in text:
            if w in alph:
                alph[w] += 1
            else:
                alph[w] = 1
        for i, w in enumerate(alph.keys()):
            probability.append((w, alph[w] / len_text))
        probability.sort(key=lambda x: x[1], reverse=True)
        return probability


root = tk.Tk()
root.title("Архиватор")
root.minsize(525, 400)
root.geometry('600x800')
root.iconphoto(False, tk.PhotoImage(file="icon.png"))

myapp = App(root)
myapp.mainloop()
