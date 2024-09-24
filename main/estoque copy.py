import tkinter as tk
from tkinter import ttk
from funcoes import LimparConsole, FecharTela
from vars import fonte


class EstoqueApplication(tk.Tk):
    LimparConsole()

    def __init__(self):
        super().__init__()
        
        cor_fundo = "#04648b"
        
        self.title("OFICIAL SPORT - Login")
        self.attributes('-fullscreen', True)  # Tela cheia        

        self.title("Gerenciamento de Estoque")
        self.state('zoomed')  # Maximiza a janela

        # Definindo estilo padrão para todos os widgets
        style = ttk.Style()
        style.configure("TButton", font=(fonte, 12))
        style.configure("TLabel", font=(fonte, 14))
        style.configure("TCombobox", font=(fonte, 12))
        style.configure("Treeview", font=(fonte, 12))
        style.configure("Treeview.Heading", font=(fonte, 14, "bold"))

        # Habilitar exibição das linhas de grade (linhas verticais e horizontais)
        style.layout("Treeview", [('Treeview.treearea', {'sticky': 'nswe'})])
        style.configure("Treeview", rowheight=25, borderwidth=1, relief="solid")

        # Frame principal
        main_frame = ttk.Frame(self, padding="3 3 12 12")
        main_frame.pack(fill=tk.BOTH)

        # Título
        title_label = ttk.Label(main_frame, text="Lista de Produtos", style="TLabel")
        title_label.pack(pady=(0, 10))

        # Frame para os botões superiores
        top_button_frame = ttk.Frame(main_frame)
        top_button_frame.pack(fill=tk.X, pady=(0, 10))

        # Função para atualizar a fonte do item selecionado no Combobox
        def on_combobox_select(event):
            selected_value = combobox.get()
            combobox.configure(font=(fonte, 12))
            print(f"Selecionado: {selected_value}")

        # Botões e Combobox com estilo
        # ttk.Button(top_button_frame, text="Sair", command=lambda: FecharTela(self)).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_button_frame, text="Sair", command=self.abrir_login).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_button_frame, text="Limpar").pack(side=tk.RIGHT, padx=5)
        
        # Combobox com evento para aplicar o estilo ao item selecionado
        combobox = ttk.Combobox(top_button_frame, values=["Selecione um grupo", "Grupo 1", "Grupo 2"], style="TCombobox")
        combobox.pack(side=tk.RIGHT, padx=5)
        combobox.bind("<<ComboboxSelected>>", on_combobox_select)  # Evento para detectar seleção

        # Tabela de produtos
        columns = ("Nome", "Descrição", "Localização", "Quantidade", "Nome Grupo", "Foto")
        tree = ttk.Treeview(main_frame, columns=columns, show='headings', style="Treeview")

        # Definir cabeçalhos
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        # Adicionar alguns dados de exemplo
        tree.insert('', tk.END, values=('DUMBBELL INJETADO 37,5KG', '600 LITROS - 300M^2 A 500M^2', 'Galpão 01', '', 'ACESSÓRIOS', ''))
        tree.insert('', tk.END, values=('DUMBBELL INJETADO 40KG', '', '', '', 'ACESSÓRIOS', ''))
        tree.insert('', tk.END, values=('CLIMATIZADOR 50.000M³/H', '', '', '', 'ACESSÓRIOS', ''))

        # Adicionar barra de rolagem
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)
        
    def abrir_login(self, event=None):
        from login import LoginApplication  # Importação local
        self.destroy()  # Fecha a janela atual
        login_app = LoginApplication()
        login_app.mainloop()     
        
    def voltar_para_login(self, event=None):
        from login import LoginApplication  # Importação local para evitar ciclo
        self.destroy()  # Fecha a janela atual
        login_app = LoginApplication()
        login_app.mainloop()        

if __name__ == "__main__":
    tela = EstoqueApplication()
    # tela.bind('<Escape>', lambda event: tela.abrir_login())
    tela.bind('<Escape>', tela.voltar_para_login)
    # tela.bind('<Escape>', lambda event: FecharTela(tela))
    tela.mainloop()
