# encoding: utf-8
import os, sys, socket, select
from Crypto.PublicKey import RSA
from Crypto import Random
from random import randint
import color
import pickle

random_generator = Random.new().read
cor = randint(1,8)
key = RSA.generate(1024, random_generator)
RECV_BUFFER = 500000

public_key = key.publickey(
def chat(host, port):
    #Transforma a string port para int para ser possivel a conexao
    port = int(port)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # Conectar ao servidor remoto
    try :
        s.connect((host, port))
    except :
        print 'Impossível conectar'
        sys.exit()

    os.system('cls' if os.name == 'nt' else 'clear') #limpar a tela
    nome = raw_input("\nOlá, seja bem vindo! Digite seu nome: ")
    print 'Conectado a um servidor remoto. Você pode começar a enviar mensagens'
    print
    #Exibe o nome do usuario sempre em preto e os outros participantes em cores diferentes
    sys.stdout.write(color.printout(nome, color.BLACK)+': '); sys.stdout.flush()
    while 1:
        socket_list = [sys.stdin, s]

        # Pega lista de sockets que são legíveis
        read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

        for sock in read_sockets:
            if sock == s:
                # Recebendo mensagem de um servidor remoto, s
                data = sock.recv(RECV_BUFFER)
                if not data :
                    print '\nDesconectado do servidor do chat'
                    sys.exit()
                else :
                    #Imprime dado
                    #data = key.decrypt(pickle.loads(data))
                    sys.stdout.write(data)
                    sys.stdout.write(color.printout(nome, color.BLACK)+': ');
                    sys.stdout.flush()

            else :
                # user entered a message
                msg = sys.stdin.readline()
            #   msg = public_key.encrypt(msg, 32)
            #   s.send(pickle.dumps(msg))
            #   sys.stdout.write(nome+': ');
                s.send(color.printout(nome, cor)+': '+msg)
                sys.stdout.write(color.printout(nome, color.BLACK)+': ');
                sys.stdout.flush()

if __name__ == "__main__":

    sys.exit(chat())
