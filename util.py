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
# Descrição util.py: Classes e métodos que realizarão todas operacoes de leitura e escrita, 
#                    criação de grupos e usuários da aplicação.
#

import socket, pdb, sys, os

MAX_CLIENTES = 10
PORT = 9010
STRING_SAIR = '$sair:$'

os.system('cls' if os.name == 'nt' else 'clear')

#Método que faz a criacao do socket utilizado trocar mensagens entre cliente e servidor
#Retorna o socket inicializado
def criar_socket(endereco):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
    s.bind(endereco)
    s.listen(MAX_CLIENTES)
    print("Servidor iniciado na porta:", PORT)
    return s

# Classe que inicializa nossa aplicacao. Na sala serão apresentadas as opções que o cliente
# deverá escolher durante a execucao do programa.
class Sala:

    #m
    def __init__(self):
        self.grupos = {} # {nome_grupo: Grupo}
        self.mapa_cliente_grupo = {} # {playerName: roomName}

    #Metodo que dá boas vindas ao novo cliente.
    def boas_vindas_novo(self, novo_cliente):
        novo_cliente.socket.sendall(b'Seja bem vindo! Digite seu nome')

    #Método que verifica se existe algum grupo criado e lista o numero de membros ativos em cada grupo
    def lista_grupos(self, cliente):
        
        if len(self.grupos) == 0:
            msg = 'Nenhum grupo ativo ainda.\n' \
                + 'Use [<grupo> nome_do_grupo] para criar um novo grupo.\n'
            cliente.socket.sendall(msg.encode())
        else:
            msg = 'Listando grupos atuais...\n'
            for grupo in self.grupos:
                msg += grupo + ": " + str(len(self.grupos[grupo].clientes)) + " membros(s)\n"
            cliente.socket.sendall(msg.encode())
    
    #Metodo que irá apresentar as instrucoes da aplicacao, e realizar manipulacoes das opcoes
    #de acordo com a escolha do usuário.
    def manipula_msg(self, cliente, msg):
        
        instrucoes = b'Instrucoes:\n'\
            + b'Use "listar-" para listar todos os grupos\n'\
            + b'Use "grupo- nome_grupo" para entrar,criar, ou mudar de um grupo\n' \
            + b'Use "manual-" para ver instrucoes\n' \
            + b'Use "sair-" para sair\n' \

        print(cliente.nome + " diz: " + msg)
        if "nome:" in msg:
            nome = msg.split()[1]
            cliente.nome = nome
            print("Nova conexao de: ", cliente.nome)
            cliente.socket.sendall(instrucoes)

        elif "grupo-" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                nome_grupo = msg.split()[1]
                if cliente.nome in self.mapa_cliente_grupo: # switching?
                    if self.mapa_cliente_grupo[cliente.nome] == nome_grupo:
                        cliente.socket.sendall(b'Voce ja esta em um grupo: ' + nome_grupo.encode())
                        same_room = True
                    else: # switch
                        old_room = self.mapa_cliente_grupo[cliente.nome]
                        self.grupos[old_room].remover_cliente(cliente)
                if not same_room:
                    if not nome_grupo in self.grupos: # mapa_cliente_grupo grupo:
                        new_room = Grupo(nome_grupo)
                        self.grupos[nome_grupo] = new_room
                    self.grupos[nome_grupo].clientes.append(cliente)
                    self.grupos[nome_grupo].boas_vindas_novo(cliente)
                    self.mapa_cliente_grupo[cliente.nome] = nome_grupo
            else:
                cliente.socket.sendall(instrucoes)

        elif "listar-" in msg:
            self.lista_grupos(cliente) 

        elif "manual-" in msg:
            cliente.socket.sendall(instrucoes)
        
        elif "sair-" in msg:
            cliente.socket.sendall(STRING_SAIR.encode())
            self.remover_cliente(cliente)

        else:
            #Se o cliente digita uma mensagem e não uma opção,
            #checa se o cliente está em um grupo antes de enviar a mensagem.
            if cliente.nome in self.mapa_cliente_grupo:
                self.grupos[self.mapa_cliente_grupo[cliente.nome]].transmissao(cliente, msg.encode())
            else:
               
                msg = 'Voce atualmente nao esta em nenhum grupo! \n' \
                    + 'Use "listar-" para ver grupos disponiveis! \n' \
                    + 'Use "grupo- nome_grupo" e junte-se a um! \n'
                cliente.socket.sendall(msg.encode())
    
    #Metodo que remove o cliente do mapa de clientes do grupo
    def remover_cliente(self, cliente):
        if cliente.nome in self.mapa_cliente_grupo:
            self.grupos[self.mapa_cliente_grupo[cliente.nome]].remover_cliente(cliente)
            del self.mapa_cliente_grupo[cliente.nome]
        print("Membro: " + cliente.nome + " deixou o grupo\n")

#Classe que irá realizar todas operacoes quando o usuário estiver dentro do grupo
class Grupo:
    def __init__(self, nome):
        self.clientes = [] # Lista de todos os sockets inicializados na aplicação
        self.nome = nome
    
    #Método que dá boas vindas ao novo cliente ingresso no grupo    
    def boas_vindas_novo(self, do_cliente):
        msg = do_cliente.nome + ' entrou no grupo\n'
        for cliente in self.clientes:
            cliente.socket.sendall(msg.encode())
    
    #Método que irá fazer o envio da mensagem para todos os clientes que estão ingressos no mesmo grupo
    def transmissao(self, do_cliente, msg):
        msg = do_cliente.nome.encode() + b":" + msg
        #PRECISA DE CORRECAO POIS ENVIA A MENSAGEM DE VOLTA AO CLIENTE QUE A ENDERECOU NO GRUPO!
        for cliente in self.clientes:
            #Tentei criar um if para não enviar mas nao resolveu 
            if cliente.socket != cliente:
                cliente.socket.send(msg)
    #Método que remove o cliente da lista de sockets inicializados na aplicacao,
    # o que significa que o cliente saiu do programa
    def remover_cliente(self, cliente):
        self.clientes.remove(cliente)
        leave_msg = cliente.nome.encode() + b" deixou o grupo\n"
        self.transmissao(cliente, leave_msg)

#Classe que inicializa o novo cliente com atributos do socket e nome para respectivas manipulacoes
#durante a execucao do programa
class Cliente:
    #Método de inicilaização do novo cliente
    def __init__(self, socket, nome = "novo cliente"):
        socket.setblocking(0)
        self.socket = socket
        self.nome = nome

    #Este método retorna o descritor de arquivo inteiro que é usado pela implementação
    #subjacente para solicitar operações I/O do sistema operacional.
    def fileno(self):
        return self.socket.fileno()
