import conexao as cn
import tkinter as tk
from tkinter import ttk
from funcoes import LimparConsole  # Assumindo que essa função é usada em outro lugar
from vars import fonte

class EstoqueApplication(tk.Tk):
    LimparConsole()

    def __init__(self):
        super().__init__()

        self.nome_grupo = None  # Inicializa a variável para armazenar a seleção do Combobox
        self.nome_produto_selecionado = None  # Variável para armazenar o nome do produto selecionado no Treeview

        self.configurar_janela()
        self.criar_estilos()
        self.criar_widgets()
        self.carregar_grupos()

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
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Lista de Produtos", style="TLabel")
        title_label.pack(pady=(0, 10))

        top_button_frame = ttk.Frame(main_frame)
        top_button_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(top_button_frame, text="Sair", command=self.voltar_para_login).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_button_frame, text="Limpar", command=self.limpar_campos).pack(side=tk.RIGHT, padx=5)

        self.combobox = ttk.Combobox(top_button_frame, values=[], style="TCombobox")
        self.combobox.pack(side=tk.RIGHT, padx=5)
        self.combobox.bind("<<ComboboxSelected>>", self.on_combobox_select)

        # Ajustando as colunas e larguras
        columns = ("Nome", "Descrição", "Localização", "Quantidade", "Nome Grupo")
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', style="Treeview")

        self.tree.heading("Nome", text="Nome")
        self.tree.column("Nome", width=150)
        self.tree.heading("Descrição", text="Descrição")
        self.tree.column("Descrição", width=200)
        self.tree.heading("Localização", text="Localização")
        self.tree.column("Localização", width=150)
        self.tree.heading("Quantidade", text="Quantidade")
        self.tree.column("Quantidade", width=100)
        self.tree.heading("Nome Grupo", text="Nome Grupo")
        self.tree.column("Nome Grupo", width=120)

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)  # Expande para ocupar todo o espaço vertical

        # Vincula o evento de seleção do Treeview
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def carregar_grupos(self):
        # Conectar ao banco de dados
        try:
            con = cn.conexao()
            sql_txt = "SELECT DISTINCT grupo FROM produtos ORDER BY grupo"
            
            # Executar a consulta
            rs = con.consultar_tree(sql_txt)
            
            # Verificar o tipo de retorno de rs
            if rs:            
                if isinstance(rs, list):
                    grupos = [row[0] for row in rs if isinstance(row, tuple) and len(row) > 0]
                else:
                    grupos = []

                self.combobox['values'] = grupos
            else:
                print("Nenhum resultado ou formato inesperado de rs.")
        except Exception as e:
            print(f"Erro ao carregar grupos: {e}")

    def carregar_produtos(self):
        if not self.nome_grupo:
            print("Nenhum grupo selecionado.")
            return

        try:
            con = cn.conexao()
            sql_txt = f"SELECT nome, descricao, localizacao, quantidade, grupo FROM produtos WHERE grupo = '{self.nome_grupo}'"

            rs = con.consultar_tree(sql_txt)

            # Limpar o Treeview antes de inserir novos dados
            for item in self.tree.get_children():
                self.tree.delete(item)

            if rs:
                for row in rs:
                    if isinstance(row, tuple):
                        self.tree.insert('', tk.END, values=row)
            else:
                print("Nenhum produto encontrado para o grupo selecionado.")
        except Exception as e:
            print(f"Erro ao carregar produtos: {e}")

    def on_combobox_select(self, event):
        self.nome_grupo = event.widget.get()  # Armazena a seleção na variável nome_grupo
        event.widget.configure(font=(fonte, 12))
        print(f"Selecionado: {self.nome_grupo}")  # Depuração: imprime o valor selecionado
        self.carregar_produtos()  # Carregar produtos para o grupo selecionado

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            self.nome_produto_selecionado = item_values[0]  # Assume que o nome do produto está na primeira posição
            print(f"Produto Selecionado: {self.nome_produto_selecionado}")  # Depuração: imprime o nome do produto selecionado

    def limpar_campos(self):
        # Limpar o Treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Limpar e recarregar o Combobox
        self.combobox.set('')  # Limpa a seleção atual do Combobox
        self.combobox['values'] = []  # Reseta os valores
        self.carregar_grupos()  # Recarrega os grupos

    def voltar_para_login(self, event=None):
        from login import LoginApplication  # Importação local para evitar ciclo
        self.destroy()  # Fecha a janela atual
        login_app = LoginApplication()
        login_app.mainloop()


if __name__ == "__main__":
    tela = EstoqueApplication()
    tela.bind('<Escape>', tela.voltar_para_login)
    tela.mainloop()
