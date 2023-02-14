import socket

IP = "127.0.0.1"
HOST_PORT = 5004
SERVICE_PORT = 5005
BUFFER_SIZE = 2048

host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_socket.bind((IP, HOST_PORT))
print("WebClient listening for connections..")
host_socket.listen()
conn, addr = host_socket.accept()
print ('Connection address:', addr)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, SERVICE_PORT))

while True:
    primljeno = conn.recv(BUFFER_SIZE).decode()
    if not primljeno: break
    print ("Received data from client:", primljeno)
    zahtev = primljeno
    client_socket.send(zahtev.encode())
    rezultat = client_socket.recv(BUFFER_SIZE)
    conn.send(rezultat)
    
client_socket.close() 
host_socket.close()