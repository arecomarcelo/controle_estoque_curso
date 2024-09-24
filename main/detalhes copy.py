import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from vars import fonte  # Supondo que 'fonte' é importado de vars
from funcoes import LimparConsole


class DetalhesApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("OFICIAL SPORT - Detalhes")
        self.attributes('-fullscreen', True)  # Tela cheia

        cor_fundo = "#04648b"

        # Frame central
        center_frame = tk.Frame(self, bg=cor_fundo, highlightbackground="white", highlightthickness=1)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Center.TFrame', background=cor_fundo)
        style.configure('TLabel', background=cor_fundo, foreground='white')
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.configure('TButton', background='#053c52', foreground='white', font=(fonte, 12))

        # Campos de texto
        ttk.Label(center_frame, text="Código Expedição:", font=(fonte, 14)).grid(row=0, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(center_frame, font=(fonte, 14)).grid(row=0, column=1, pady=5)

        ttk.Label(center_frame, text="Nome:", font=(fonte, 14)).grid(row=1, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(center_frame, font=(fonte, 14)).grid(row=1, column=1, pady=5)

        ttk.Label(center_frame, text="Descrição:", font=(fonte, 14)).grid(row=2, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(center_frame, font=(fonte, 14)).grid(row=2, column=1, pady=5)

        ttk.Label(center_frame, text="Grupo:", font=(fonte, 14)).grid(row=3, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(center_frame, font=(fonte, 14)).grid(row=3, column=1, pady=5)

        ttk.Label(center_frame, text="Estoque:", font=(fonte, 14)).grid(row=4, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Entry(center_frame, font=(fonte, 14)).grid(row=4, column=1, pady=5)

        # Botões de Entrada e Saída
        ttk.Button(center_frame, text="Entrada", style='TButton').grid(row=4, column=2, padx=5)
        ttk.Button(center_frame, text="Saída", style='TButton').grid(row=4, column=3, padx=5)

        ttk.Label(center_frame, text="Localização:", font=(fonte, 14)).grid(row=5, column=0, sticky=tk.W, padx=20, pady=5)
        ttk.Combobox(center_frame, font=(fonte, 14)).grid(row=5, column=1, pady=5)

        # Seção de imagem
        image_frame = tk.Frame(center_frame, bg=cor_fundo)
        image_frame.grid(row=0, column=2, rowspan=6, padx=20)

        image_placeholder = tk.Label(image_frame, text="Sem Imagem", bg=cor_fundo, fg='white')
        image_placeholder.pack()

        ttk.Button(image_frame, text="Escolher Arquivo", style='TButton').pack(pady=5)
        ttk.Button(image_frame, text="Carregar Imagem", style='TButton').pack()

        # Botões de Atualizar e Retornar
        button_frame = ttk.Frame(center_frame, style='Center.TFrame')
        button_frame.grid(row=6, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(button_frame, text="Atualizar", style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Retornar", style='TButton').pack(side=tk.RIGHT)

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

if __name__ == "__main__":
    tela_detalhes = DetalhesApplication()
    tela_detalhes.bind('<F11>', tela_detalhes.toggle_fullscreen)
    tela_detalhes.bind('<Escape>', lambda event: tela_detalhes.quit_fullscreen())
    tela_detalhes.mainloop()
