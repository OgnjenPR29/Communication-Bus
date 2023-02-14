import socket
from sqllite_baza import baza_podataka

baza = baza_podataka()
path = 'resurs.db'
con = baza.create_connection(path)

IP = "127.0.0.1"
HOST_PORT = 5008
BUFFER_SIZE = 2048

host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_socket.bind((IP, HOST_PORT))
print("Repository listening for connections..")
host_socket.listen()

conn, addr = host_socket.accept()
print ('Connection address:', addr)

while True:
    primljeno = conn.recv(BUFFER_SIZE).decode()
    if not primljeno: break
    print ("Received data from client:", primljeno)
    zahtev = primljeno
    odgovor = baza.execute_query(con,zahtev)
    out = [item for t in odgovor for item in t]
    odgovorStr = ' '.join(str(elem) for elem in out)
    if odgovorStr == "":
        odgovorStr = "EMPTY"
        print(odgovorStr)
    conn.sendall(odgovorStr.encode())