import json
import socket
from warnings import catch_warnings

IP = "127.0.0.1"
SERVICE_PORT = 5004
BUFFER_SIZE = 2048

f = open ('zahtevi.json', "r")

try:
    data = json.loads(f.read())
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, SERVICE_PORT))

    for i in data:
        #json.dumps formatira u json, inace se zamene " sa ' pri citanju iz fajla
        zahtev = json.dumps(i)
        client_socket.send(zahtev.encode())
        rezultat = client_socket.recv(BUFFER_SIZE).decode()
        print(rezultat)

    client_socket.close()
except:
    print('FAJL NIJE U JSON FORMATU!')
f.close()




