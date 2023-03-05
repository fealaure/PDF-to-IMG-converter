import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image
import fitz

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.folder_path = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        self.progress_var.set(0)

        self.folder_label = tk.Label(self, text="Pasta de origem:")
        self.folder_label.pack(pady=(20, 0))

        self.folder_entry = tk.Entry(self, textvariable=self.folder_path, width=50)
        self.folder_entry.pack(pady=(0, 10))

        self.folder_button = tk.Button(self, text="Selecionar Pasta", command=self.select_folder)
        self.folder_button.pack(pady=(0, 20))

        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=20)

        self.start_button = tk.Button(self, text="Iniciar", command=self.process_files)
        self.start_button.pack(pady=(20, 0))

    def select_folder(self):
        self.folder_path.set(filedialog.askdirectory())

    def process_files(self):
        if not self.folder_path.get():
            tk.messagebox.showerror("Erro", "Selecione uma pasta de origem.")
            return

        total_files = 0
        processed_files = 0

        for dirpath, dirnames, filenames in os.walk(self.folder_path.get()):
            for filename in filenames:
                if filename.endswith('.pdf'):
                    total_files += 1

        for dirpath, dirnames, filenames in os.walk(self.folder_path.get()):
            for filename in filenames:
                if filename.endswith('.pdf'):
                    input_path = os.path.join(dirpath, filename)
                    output_path = os.path.join(dirpath, f"{os.path.splitext(filename)[0]}.jpg")

                    with fitz.open(input_path) as pdf:
                        page = pdf[0]
                        pix = page.get_pixmap()
                        image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                        with open(output_path, 'wb') as output_file:
                            image.save(output_file, "JPEG")

                    processed_files += 1
                    self.progress_var.set(processed_files / total_files * 100)
                    self.update()

        self.progress_var.set(0)
        tk.messagebox.showinfo("Concluído", "Extração de capas concluída com sucesso.")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
