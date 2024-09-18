import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from enumeradores import Direcao
from vars import nome_aplicacao, img_icone_principal

class Error(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def LimparConsole():
    os.system('cls')
    
def PosicionaBotao (tela, botao_anterior, botao_atual, direcao = Direcao.DIREITA):
    tela.update_idletasks()
    
    width = botao_anterior.winfo_width() + 5
    
    if direcao.name == "ESQUERDA":
        posx = botao_anterior.winfo_x() + width
    else:
        posx = botao_anterior.winfo_x() - width
    
    posy = botao_anterior.winfo_y()    
    
    botao_atual.place(x = posx, y = posy, width = 100)         

def AbreTela(arquivo):
    exec(open(f"main\\{arquivo}", encoding="utf-8").read(),locals())
    
def sobre():
    messagebox.showinfo("Sobre", "Sistema Comercial 1.0")
    
def sair(tela):
    var_sair = messagebox.askyesno("Sair", "Tem certeza que deseja sair?")
    if var_sair:
        tela.destroy()
               
def MontaTela(cor_fundo, imagem, titulo, principal = False):
    if principal:
        tela = tk.Tk()
    else:
        tela = tk.Toplevel()    
        
    tela.geometry('1960x800+0+0')
    tela.state('zoomed')
    tela.title(f"{nome_aplicacao} - {titulo}")
    tela['bg'] = cor_fundo
    
    icone_imagem = Image.open(img_icone_principal)
    icone_tkimage = ImageTk.PhotoImage(icone_imagem)

    tela.iconphoto(False, icone_tkimage)
    tkimage = ImageTk.PhotoImage(Image.open(imagem).resize((tela.winfo_screenwidth(), tela.winfo_screenheight())))
    label = tk.Label(tela, image=tkimage)
    label.image = tkimage
    label.pack()

    return tela

def CriarBotao(tela, imagem, texto):
    imagem = Image.open(imagem)
    imagem = imagem.resize((50, 50))
    tkimage = ImageTk.PhotoImage(imagem)

    botao = tk.Button(tela, text=texto, image=tkimage, compound='left', command=lambda: print("Botão clicado!"))
    botao.image = tkimage
    botao.pack(pady=20)


def FecharTela(tela, event=None):
    tela.destroy()