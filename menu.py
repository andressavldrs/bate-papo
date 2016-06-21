import client, sys, subprocess
import threading
from threading import Thread
from random import randint

print (30 * '-')
print ("   B A T E - P A P O    ")
print (30 * '-')
print ("1. Criar uma sala ")
print ("2. Entrar em uma sala ")
print ("3. Sair")
print (30 * '-')

## Get input ###
choice = raw_input('Digite a sua escolha [1-3] : ')

### Convert string to int type ##
choice = int(choice)

### Take action as per selected menu-option ###
while choice != 3:
    if choice == 1:
        #Cria uma nova sala (porta) para conexao
        port = randint(4000, 9000)
        print port
        #Cria um server nesse com essa porta, mas nao mantem o menu aberto
        subprocess.Popen(["python", "server.py", str(port)])
        chat_client.chat_client("localhost", port)
    elif choice == 2:
        #Você deve saber em que sala deseja entrar
        port = raw_input('Digite a sala que deseja entrar: ')
        client.chat("localhost", port)
    elif choice == 3:
        #Sai do menu
        print ("Tchau!")
    else:    ## default ##
        print ("Opção inválida. Tente novamente...")
