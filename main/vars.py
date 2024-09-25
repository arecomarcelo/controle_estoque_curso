import os
from datetime import datetime, timedelta

# -- Variáveis de Caminhos ---    ############################
caminhoAplicacao = f"{os.path.dirname(os.path.dirname(__file__))}\\"
caminhoImagens = caminhoAplicacao.replace(r'/', "\\") + 'imagens\\'

# -- Variáveis de Imagens ---    ############################
img_icone_principal = f"{caminhoImagens}icone.ico"
img_logo = f"{caminhoImagens}logo.png"
img_background = f"{caminhoImagens}walpaper.png"

QuebraLinha = "\n"

nome_aplicacao = "Controle de Estoque 1.0"
cor = "WhiteSmoke"
cor_fundo="black"
cor_fonte="WhiteSmoke"
fonte = "Roboto"


