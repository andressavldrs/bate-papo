# -*- coding: utf-8 -*-
#
# Tema 2: Bate papo (Servidor e Cliente)
#
# Descrição: Fornecer servidor e cliente de mensagens, criação de grupos, gerenciamento
#            de contas de usuários e grupos; !envio de arquivos; !bloquear usuários; 
#            !Comunicação criptografada entre os clientes;
#
#Participantes: 
#13/0042943  ANDRESSA RODRIGUES ALVES GALVAO VALADARES
#14/0138374  FELIPE CORDEIRO PIRES MAGALHÃES
#13/0143880  MARCELLA PANTAROTTO
#12/0077019  MATEUS NOGUEIRA BRUMANO CASTRO
#10/0123571  SILAS SOUZA FERNANDES
#
# Descrição cliente.py: Estabelecer conexão com o servidor. Utiliza-se das classes e métodos
#                       do arquivo util.py para realizar todas operações inerentes da aplicacao.
#

import select, socket, sys, os
from util import Grupo, Sala, Cliente
import util

BUFFER_LEITURA = 9010
host = ''

conexao_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conexao_servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
conexao_servidor.connect((host, util.PORT))

os.system('cls' if os.name == 'nt' else 'clear')

def prompt():
    print(': ', end=' ', flush = True)

print("Conectado ao servidor\n")
msg_prefix = ''

lista_socket = [sys.stdin, conexao_servidor]

while True:
    # Cliente.fileno() descrito no util.py utilizado para operacoes de I/O no SO
    sockets_leitura, sockets_escrita, erro_sockets = select.select(lista_socket, [], [])
    for s in sockets_leitura:
        if s is conexao_servidor: 
            msg = s.recv(BUFFER_LEITURA)
            if not msg:
                print("O servidor caiu!")
                sys.exit(2)
            else:
                if msg == util.STRING_SAIR.encode():
                    sys.stdout.write('Ate logo!\n')
                    sys.exit(2)
                else:
                    sys.stdout.write(msg.decode())
                    if 'Digite seu nome' in msg.decode():
                        msg_prefix = 'nome: ' 
                    else:
                        msg_prefix = ''
                    prompt()

        else:
            msg = msg_prefix + sys.stdin.readline()
            conexao_servidor.sendall(msg.encode())
