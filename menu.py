import client, server, sys
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
#while choice != 3:
if choice == 1:
    port = randint(4000, 9000)
    print port
    Thread(target = server.chat(port)).start()
    Thread(target = client.chat("localhost", port)).start()
    #sys.argv = ['chat_server.py', port]
    #execfile('chat_server.py')
    #chat_client.chat_client("localhost", 01)
elif choice == 2:
    client.chat("localhost", port)
elif choice == 3:
    print ("Tchau!")
else:    ## default ##
    print ("Invalid number. Try again...")
