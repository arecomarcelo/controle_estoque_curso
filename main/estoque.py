import tkinter as tk
from tkinter import ttk
from funcoes import LimparConsole  # Assumindo que essa função é usada em outro lugar
from vars import fonte


class EstoqueApplication(tk.Tk):
    LimparConsole()

    def __init__(self):
        super().__init__()

        self.configurar_janela()
        self.criar_estilos()
        self.criar_widgets()

    def configurar_janela(self):
        self.title("Gerenciamento de Estoque")
        self.attributes('-fullscreen', True)  # Tela cheia
        self.state('zoomed')  # Maximiza a janela

    def criar_estilos(self):
        style = ttk.Style()
        style.configure("TButton", font=(fonte, 12))
        style.configure("TLabel", font=(fonte, 14))
        style.configure("TCombobox", font=(fonte, 12))
        style.configure("Treeview", font=(fonte, 12))
        style.configure("Treeview.Heading", font=(fonte, 14, "bold"))
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")

    def criar_widgets(self):
        main_frame = ttk.Frame(self, padding="3 3 12 12")
        main_frame.pack(fill=tk.BOTH)

        title_label = ttk.Label(main_frame, text="Lista de Produtos", style="TLabel")
        title_label.pack(pady=(0, 10))

        top_button_frame = ttk.Frame(main_frame)
        top_button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(top_button_frame, text="Sair", command=self.voltar_para_login).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_button_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.RIGHT, padx=5)

        combobox = ttk.Combobox(top_button_frame, values=["Selecione um grupo", "Grupo 1", "Grupo 2"], style="TCombobox")
        combobox.pack(side=tk.RIGHT, padx=5)
        combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        columns = ("Nome", "Descrição", "Localização", "Quantidade", "Nome Grupo", "Foto")
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', style="Treeview")

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        tree.insert('', tk.END, values=('DUMBBELL INJETADO 37,5KG', '600 LITROS - 300M^2 A 500M^2', 'Galpão 01', '', 'ACESSÓRIOS', ''))
        tree.insert('', tk.END, values=('DUMBBELL INJETADO 40KG', '', 'ACESSÓRIOS', ''))
        tree.insert('', tk.END, values=('CLIMATIZADOR 50.000M³/H', '', 'ACESSÓRIOS', ''))

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

    def on_combobox_select(self, event):
        selected_value = event.widget.get()
        event.widget.configure(font=(fonte, 12))
        print(f"Selecionado: {selected_value}")

    def limpar_campos(self):
        # Implementar a lógica para limpar campos ou tabela
        pass

    def voltar_para_login(self, event=None):
        from login import LoginApplication  # Importação local para evitar ciclo
        self.destroy()  # Fecha a janela atual
        login_app = LoginApplication()
        login_app.mainloop()


if __name__ == "__main__":
    tela = EstoqueApplication()
    tela.bind('<Escape>', tela.voltar_para_login)
    tela.mainloop()
