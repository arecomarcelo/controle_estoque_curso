import os
class Error(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

def LimparConsole():
    os.system('cls')                  

def FecharTela(tela, event=None):
    tela.destroy()