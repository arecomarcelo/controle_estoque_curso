# -- coding: cp1252 --
import sys
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from funcoes import MontaTela, LimparConsole, PosicionaBotao, FecharTela, Error, AbreTela
from vars import *
# import conexao as cn

LimparConsole()

##Configura Tela
cor_fundo = "black"
cor_fonte = "WhiteSmoke"
fonte = "Roboto"
tela_login = MontaTela(cor_fundo,img_background, "Login do Sistema", True)
##Configura Tela


def menu():
    tela_login.destroy()
    AbreTela("menu.py") 
    
def validasenha():

    var_login = txtusuario.get()
    var_senha = txtsenha.get()

    try:
        con=cn.conexao()
        
        sql_txt=(f"select usuario, nome from login where usuario = '{var_login}'"
                 + f"and CAST(aes_decrypt(senha,'chave') as char) = '{var_senha}'")
                 
        rs=con.consultar(sql_txt)
       
        if rs:
            print("teste")
            lblresult = tk.Label(tela_login, text ="**** Acesso Permitido ***", foreground='blue')
            lblresult.place(x = 125, y = 110)
            con.fechar()

            menu()          
        else:
           lblresult = tk.Label(tela_login, text ="Usuario ou Senha Invalida", foreground='red')
           lblresult.place(x = 125, y = 130)              
    except Error:
        # db.rollback()
        print(Error)
        
    con.fechar()
    
def mostarsenha():
    if txtsenha.cget('show') == '':
        txtsenha.config(show='*')
        btnmostrar.config(text='Mostrar Senha')
    else:
        txtsenha.config(show='')
        btnmostrar.config(text='Enconder Senha')
        

##Implementa Controles
lblUsuario = tk.Label(tela_login, text ="Usuario:", bg=cor_fundo, fg=cor_fonte, font=(fonte, 12), anchor = "e")
lblUsuario.place(x = 50, y = 50, width = 80, height=25)

txtusuario = tk.Entry(tela_login, font=(fonte, 12), width = 35)
txtusuario.place(x = 150, y = 50, width = 100, height=25)

lblsenha = tk.Label(tela_login, text ="Senha:  ", bg=cor_fundo, fg=cor_fonte, font=(fonte, 12), anchor = "e")
lblsenha.place(x = 50, y = 100, width = 80, height=25)
 
txtsenha  = tk.Entry(tela_login, font=(fonte, 12), width = 35, show = "*")
txtsenha.place(x = 150, y = 100, width = 100, height=25)

btnsubmeter = tk.Button(tela_login, text ="Login", 
                      bg ='black',foreground='white', font=(fonte, 12, 'bold'), command=validasenha)
btnsubmeter.place(x = 170, y = 150, width = 55, height=25)

btnmostrar = tk.Button(tela_login, text ="Mostrar Senha", 
                      bg ='white',foreground='black', font=(fonte, 12, 'bold'), command=mostarsenha)
btnmostrar.place(x = 270, y = 100, width = 120, height=25)
##Implementa Controles

txtusuario.focus_set()

tela_login.mainloop()