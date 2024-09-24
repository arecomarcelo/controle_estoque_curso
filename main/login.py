import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from vars import img_background, img_logo, fonte
from funcoes import FecharTela, Error
import conexao as cn

class LoginApplication(tk.Tk):
    
    def __init__(self):
        super().__init__()       
        
        cor_fundo = "#04648b"
        
        self.title("OFICIAL SPORT - Login")
        self.attributes('-fullscreen', True)  # Tela cheia

        bg_image = Image.open(img_background)
        bg_image = bg_image.resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)

        bg_label = tk.Label(self, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Frame central
        center_frame = tk.Frame(self, bg=cor_fundo, highlightbackground="white", highlightthickness=1)
        center_frame.place(relx=0.5, rely=0.5, anchor='center')

        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('Center.TFrame', background=cor_fundo)
        style.configure('TLabel', background=cor_fundo, foreground='white')
        style.configure('TEntry', fieldbackground='white', foreground='black')
        style.configure('logar.TButton', background='#053c52', foreground='white', font=(fonte, 12))
        style.configure('sair.TButton', background='#053c52', foreground='white', font=(fonte, 12))

        logo_img = Image.open(img_logo)
        logo_img = logo_img.resize((120, 100))  # Ajuste o tamanho conforme necessário
        logo = ImageTk.PhotoImage(logo_img)
        logo_label = ttk.Label(center_frame, image=logo, background=cor_fundo)
        logo_label.image = logo
        logo_label.pack(pady=(20, 10))

        # Campo de usuário
        user_label = ttk.Label(center_frame, text="Usuário:", font=(fonte, 14))
        user_label.pack(anchor=tk.W, padx=20)
        self.user_entry = ttk.Entry(center_frame, font=(fonte, 14))
        self.user_entry.pack(pady=(0, 10), padx=20)

        # Campo de senha
        pass_label = ttk.Label(center_frame, text="Senha:", font=(fonte, 14))
        pass_label.pack(anchor=tk.W, padx=20)
        self.pass_entry = ttk.Entry(center_frame, show="*", font=(fonte, 14))
        self.pass_entry.pack(pady=(0, 20), padx=20)

        # Frame para os botões
        button_frame = ttk.Frame(center_frame, style='Center.TFrame')
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

        # Botão de acesso
        logar_button = ttk.Button(button_frame, text="Logar", style='logar.TButton', width=10, command=self.on_login)
        logar_button.grid(row=0, column=0, padx=(0, 10), pady=(0, 5))

        # Botão de sair
        sair_button = ttk.Button(button_frame, text="Sair", style='sair.TButton', width=10, command=lambda: FecharTela(self))
        sair_button.grid(row=0, column=1, padx=(10, 0), pady=(0, 5))

        # Botão de cadastrar
        cadastrar_button = ttk.Button(button_frame, text="Cadastrar", style='logar.TButton', width=10, command=self.cadastrar)
        cadastrar_button.grid(row=1, column=0, padx=(0, 10), pady=(5, 0))

        # Botão de limpar
        limpar_button = ttk.Button(button_frame, text="Limpar", style='logar.TButton', width=10, command=self.limpar)
        limpar_button.grid(row=1, column=1, padx=(10, 0), pady=(5, 0))

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

    def on_login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showwarning("Aviso", "Usuário e senha não podem estar vazios", parent=self)
            return

        if self.verificar_login(username, password):
            self.abrir_estoque()

    def verificar_login(self, username, password):
        try:
            con = cn.conexao()
            
            sql_txt=(f"select usuario, senha from usuarios where usuario = '{username}'"
                    + f"and senha = SHA2('{password}', 256)")
            rs=con.consultar(sql_txt)
        
            if rs:
                return True
            else:
                messagebox.showerror("Aviso", "Usuario ou Senha Inválidos", parent=self)
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}", parent=self)
        finally:
            con.fechar()        
        
        return False

    def abrir_estoque(self):
        self.destroy()  # Fecha a janela atual
        from estoque import EstoqueApplication  # Importação local para evitar ciclo
        estoque_app = EstoqueApplication()
        estoque_app.mainloop()
        

    def cadastrar(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
    
        con=cn.conexao()
        
        sql_txt = f"select usuario, senha from usuarios where usuario = '{username}'"

        rs=con.consultar(sql_txt)

        if rs:
            sql_text = f"update usuarios set usuario='{username}', senha = SHA2('{password}', 256) where usuario = '{username}'"
        else:
            sql_text = f"insert into usuarios (usuario, senha) values ('{username}',SHA2('{password}', 256))"
            

        if con.gravar(sql_text):
            messagebox.showinfo("Aviso", "Usuário Gravado ou Atualizado com Sucesso")
            self.limpar()
        else:
            messagebox.showerror("Erro", "Houve um Erro na Gravação")

        con.fechar()
        
    def limpar(self):
        # Limpa os campos de entrada
        self.user_entry.delete(0, tk.END)
        self.pass_entry.delete(0, tk.END)        



if __name__ == "__main__":
    tela = LoginApplication()
    tela.bind('<F11>', tela.toggle_fullscreen)
    tela.bind('<Escape>', lambda event: FecharTela(tela))
    tela.mainloop()
