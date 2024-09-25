import tkinter as tk
from tkinter import ttk, messagebox
from vars import fonte
import conexao as cn

class DetalhesApplication(tk.Tk):
    def __init__(self, nome_produto):
        super().__init__()

        self.title("OFICIAL SPORT - Detalhes")
        self.attributes('-fullscreen', True)

        cor_fundo = "#d4cdcd"

        # Configuração da cor de fundo da janela principal
        self.configure(bg=cor_fundo)

        center_frame = tk.Frame(self, bg="#bfbdbd", highlightbackground="white", highlightthickness=0.5)
        center_frame.place(relx=0.5, rely=0.5, anchor='center', width=750, height=285)

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure("TButton", font=(fonte, 12))
        style.configure("TLabel", font=(fonte, 14), background="#bfbdbd")
        style.configure("TCombobox", font=(fonte, 14))

        # Campos de texto
        ttk.Label(center_frame, text="Código Expedição:", style='TLabel', anchor=tk.E).grid(row=0, column=0, sticky=tk.E, padx=10, pady=5)
        self.codigo_entry = ttk.Entry(center_frame, font=(fonte, 14), width=50)
        self.codigo_entry.grid(row=0, column=1, sticky=tk.W, pady=5)

        ttk.Label(center_frame, text="Nome:", style='TLabel', anchor=tk.E).grid(row=1, column=0, sticky=tk.E, padx=10, pady=5)
        self.nome_entry = ttk.Entry(center_frame, font=(fonte, 14), width=50)
        self.nome_entry.grid(row=1, column=1, sticky=tk.W, pady=5)
        self.nome_entry.insert(0, nome_produto)

        ttk.Label(center_frame, text="Descrição:", style='TLabel', anchor=tk.E).grid(row=2, column=0, sticky=tk.E, padx=10, pady=5)
        self.descricao_entry = ttk.Entry(center_frame, font=(fonte, 14), width=50)
        self.descricao_entry.grid(row=2, column=1, sticky=tk.W, pady=5)

        ttk.Label(center_frame, text="Grupo:", style='TLabel', anchor=tk.E).grid(row=3, column=0, sticky=tk.E, padx=10, pady=5)
        self.grupo_entry = ttk.Entry(center_frame, font=(fonte, 14), width=50)
        self.grupo_entry.grid(row=3, column=1, sticky=tk.W, pady=5)

        ttk.Label(center_frame, text="Estoque:", style='TLabel', anchor=tk.E).grid(row=4, column=0, sticky=tk.E, padx=10, pady=5)
        self.estoque_entry = ttk.Entry(center_frame, font=(fonte, 14), width=20)
        self.estoque_entry.grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(center_frame, text="Localização:", style='TLabel', anchor=tk.E).grid(row=5, column=0, sticky=tk.E, padx=10, pady=5)
        self.localizacao_combobox = ttk.Combobox(center_frame, font=(fonte, 14), width=30)
        self.localizacao_combobox['values'] = ("Galpão 01", "Galpão 02")
        self.localizacao_combobox.grid(row=5, column=1, sticky=tk.W, pady=5)

        # Botões de Excluir, Atualizar e Retornar
        style.configure("Custom.TFrame", background="#bfbdbd")
        button_frame = ttk.Frame(center_frame, style="Custom.TFrame")
        button_frame.grid(row=6, column=0, columnspan=4, pady=(10, 0))

        ttk.Button(button_frame, text="Excluir", style='TButton', command=self.excluir_produto).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Atualizar", style='TButton', command=self.atualizar_produto).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Retornar", style='TButton', command=self.retornar_para_estoque).pack(side=tk.RIGHT)

        # Carregar dados do produto
        self.carregar_dados(nome_produto)

    def carregar_dados(self, nome_produto):
        con = cn.conexao()
        sql_txt = f"SELECT nome, descricao, codigo_expedicao, grupo, quantidade, localizacao FROM produtos WHERE nome = '{nome_produto}'"
        rs = con.consultar_tree(sql_txt)

        if rs and isinstance(rs, list) and len(rs) > 0:
            row = rs[0]
            if isinstance(row, tuple) and len(row) == 6:
                self.nome_entry.delete(0, tk.END)
                self.descricao_entry.delete(0, tk.END)
                self.codigo_entry.delete(0, tk.END)
                self.grupo_entry.delete(0, tk.END)
                self.estoque_entry.delete(0, tk.END)

                self.nome_entry.insert(0, row[0])
                self.descricao_entry.insert(0, row[1])
                self.codigo_entry.insert(0, row[2])
                self.grupo_entry.insert(0, row[3])
                self.estoque_entry.insert(0, row[4])
                self.localizacao_combobox.set(row[5])
            else:
                messagebox.showinfo("Erro", "Formato Inesperado de Dados ou Dados Insuficientes.")
        else:
            messagebox.showinfo("Erro", "Nenhum Dado Encontrado para o Produto Selecionado.")

    def atualizar_produto(self):
        descricao = self.descricao_entry.get()
        codigo_expedicao = self.codigo_entry.get()
        grupo = self.grupo_entry.get()
        quantidade = self.estoque_entry.get()
        localizacao = self.localizacao_combobox.get()
        nome = self.nome_entry.get()

        try:
            con = cn.conexao()
                       
            sql_txt = (f"UPDATE produtos "
                       f"SET descricao='{descricao}', codigo_expedicao='{codigo_expedicao}', grupo='{grupo}', "
                       f"quantidade={quantidade}, localizacao='{localizacao}' "
                       f"WHERE nome='{nome}'")
            
            con.executar(sql_txt)
            
            messagebox.showinfo("Informação", f"Produto: {nome} \n Atualizado com Sucesso.")
            
            self.retornar_para_estoque()  # Retorna para a tela de estoque
        except Exception as e:
            messagebox.showinfo("Erro", f"Erro ao Atualizar o Produto: {e}")

    def excluir_produto(self):
        nome = self.nome_entry.get()
        if messagebox.askyesno("Confirmação", f"Tem Certeza de que Deseja excluir\n o produto '{nome}'?"):
            try:
                con = cn.conexao()
                sql_txt = f"DELETE FROM produtos WHERE nome='{nome}'"
                con.executar(sql_txt)
                messagebox.showinfo("Informação", f"Produto: {nome} \n Excluído com Sucesso.")
                self.retornar_para_estoque()  # Retorna para a tela de estoque
            except Exception as e:
                messagebox.showinfo("Erro", f"Erro ao Excluir o Produto: {e}")

    def retornar_para_estoque(self):
        self.destroy()  # Fecha a janela atual
        from estoque import EstoqueApplication  # Importação local para evitar o ciclo
        EstoqueApplication().mainloop()  # Abre a aplicação de estoque

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

if __name__ == "__main__":
    tela_detalhes = DetalhesApplication("")
    tela_detalhes.bind('<F11>', tela_detalhes.toggle_fullscreen)
    tela_detalhes.bind('<Escape>', lambda event: tela_detalhes.retornar_para_estoque())
    tela_detalhes.mainloop()
