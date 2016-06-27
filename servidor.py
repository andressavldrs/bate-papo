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
# Descrição servidor.py: Incializa o servidor que irá receber as mensagens e endereçar aos clientes
#                        corretos, definidos na lista de sockets do grupo que o cliente pertence.
#

import select, socket, sys,os, pdb 
from util import Grupo, Sala, Cliente
import util

BUFFER_LEITURA = 1024

host = ''
escuta_sock = util.criar_socket((host, util.PORT))

sala = Sala()
lista_conexoes = []
lista_conexoes.append(escuta_sock)

while True:
    # Cliente.fileno() descrito no util.py utilizado para operacoes de I/O no SO
    clientes_leitura, clientes_escrita, erro_sockets = select.select(lista_conexoes, [], [])
    for cliente in clientes_leitura:
        if cliente is escuta_sock: # Nova conexão
            novo_socket, add = cliente.accept()
            novo_cliente = Cliente(novo_socket)
            lista_conexoes.append(novo_cliente)
            sala.boas_vindas_novo(novo_cliente)

        else: # Recebe uma nova mensagem
            msg = cliente.socket.recv(BUFFER_LEITURA)
            if msg:
                msg = msg.decode().lower()
                sala.manipula_msg(cliente, msg)
            else:
                cliente.socket.close()
                lista_conexoes.remove(cliente)

    for sock in erro_sockets: # Socket na lista de sockets com erro, fecha socket.
        sock.close()
        lista_conexoes.remove(sock)