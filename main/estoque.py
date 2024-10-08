import conexao as cn
import tkinter as tk
from tkinter import ttk, messagebox
from funcoes import LimparConsole
from vars import fonte
from detalhes import DetalhesApplication

class EstoqueApplication(tk.Tk):
    LimparConsole()

    def __init__(self):
        super().__init__()

        self.nome_grupo = None
        self.nome_produto_selecionado = None

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
        self.combobox.config(width=30, font=(fonte, 14))
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

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def carregar_grupos(self):
        try:
            con = cn.conexao()
            sql_txt = "SELECT DISTINCT grupo FROM produtos ORDER BY grupo"
            
            rs = con.consultar_tree(sql_txt)
            
            if rs:            
                if isinstance(rs, list):
                    grupos = [row[0] for row in rs if isinstance(row, tuple) and len(row) > 0]
                else:
                    grupos = []

                self.combobox['values'] = grupos
            else:
                messagebox.showinfo("Erro", "Nenhum Resultado ou Formato Inesperado de Dados.")
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao carregar Grupos: {e}")

    def carregar_produtos(self):
        if not self.nome_grupo:
            messagebox.showinfo("Erro", "Nenhum Grupo Selecionado.")
            return

        try:
            con = cn.conexao()
            sql_txt = f"SELECT nome, descricao, localizacao, quantidade, grupo FROM produtos WHERE grupo = '{self.nome_grupo}'"

            rs = con.consultar_tree(sql_txt)

            for item in self.tree.get_children():
                self.tree.delete(item)

            if rs:
                for row in rs:
                    if isinstance(row, tuple):
                        self.tree.insert('', tk.END, values=row)
            else:
                messagebox.showinfo("Informação", "Nenhum Produto Encontrado para o Grupo Selecionado.")
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao Carregar Produtos: {e}")

    def on_combobox_select(self, event):
        self.nome_grupo = event.widget.get() # Armazena a seleção na variável nome_grupo
        event.widget.configure(font=(fonte, 12))

        self.carregar_produtos()  # Carregar produtos para o grupo selecionado

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item, 'values')
            self.nome_produto_selecionado = item_values[0]
            
            # Fecha a janela atual e abre a nova janela de detalhes
            self.destroy()
            DetalhesApplication(self.nome_produto_selecionado)

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
