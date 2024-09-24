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
        button_frame.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Botão de acesso
        logar_button = ttk.Button(button_frame, text="Logar", style='logar.TButton', width=10, command=self.on_login)
        logar_button.pack(side=tk.LEFT, padx=(0, 10))

        # Botão de sair
        sair_button = ttk.Button(button_frame, text="Sair", style='sair.TButton', command=lambda: FecharTela(self))
        sair_button.pack(side=tk.RIGHT)

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def quit_fullscreen(self, event=None):
        self.attributes('-fullscreen', False)

    def on_login(self):
        username = self.user_entry.get()
        password = self.pass_entry.get()

        if self.verificar_login(username, password):
            self.abrir_estoque()

    def verificar_login(self, username, password):
        try:
            con=cn.conexao()
            
            sql_txt=(f"select usuario, senha from usuarios where usuario = '{username}'"
                    + f"and senha = SHA2('{password}', 256)")
                    
            rs=con.consultar(sql_txt)
        
            if rs:
                return True
            else:
                 messagebox.showerror("Aviso", "Usuario ou Senha Inválidos",parent = self)
        except Error:
            print(Error)
            
        con.fechar()        
        
        return False

    def abrir_estoque(self):
        self.destroy()  # Fecha a janela atual
        from estoque import EstoqueApplication  # Importação local para evitar ciclo
        estoque_app = EstoqueApplication()
        estoque_app.mainloop()

if __name__ == "__main__":
    tela = LoginApplication()
    tela.bind('<F11>', tela.toggle_fullscreen)
    tela.bind('<Escape>', lambda event: FecharTela(tela))
    tela.mainloop()
