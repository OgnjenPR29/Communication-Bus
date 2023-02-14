import socket
import json
import re

verb_format = ["GET", "POST", "PATCH","DELETE"]
noun_format = ["/resurs/1","/resurs/2","/resurs/3","/resurs/4"]

query_fields1 = ["id","name","surname","description","type",""]
query_fields2 = ["id","title",""]
query_fields3 = ["id","idFirstUser","idSecondUser","type",""]
query_fields4 = ["id","title",""]

IP = "127.0.0.1"
HOST_PORT = 5005
SERVICE_PORT_XMLADAPTER = 5006
SERVICE_PORT_DATABASE_ADAPTER = 5007
BUFFER_SIZE = 2048


def switch(noun):
    if noun[-1] == '1':
        query_fields = query_fields1
    if noun[-1] == '2':
        query_fields = query_fields2
    if noun[-1] == '3':
        query_fields = query_fields3
    if noun[-1] == '4':
        query_fields = query_fields4
    return query_fields

def provera_verb(zahtev_dict):
    if "verb" not in zahtev_dict:
        return False
    return zahtev_dict["verb"] in verb_format

def provera_noun(zahtev_dict):
    if "noun" not in zahtev_dict:
        return False
    return zahtev_dict["noun"] in noun_format

def provera_query(zahtev_dict):
    if "query" not in zahtev_dict:
        return False
    noun = zahtev_dict["noun"]
    
    query_fields = switch(noun)

    query_statement = re.split("=|; ",zahtev_dict["query"])

    for j in range(len(query_statement)):
        if(j%2==0 and (query_statement[j] not in query_fields)):
            return False
            
    return True

def provera_fields(zahtev_dict):
    if "fields" not in zahtev_dict:
        return False
    noun = zahtev_dict["noun"]
    
    fields = switch(noun)

    if zahtev_dict["verb"] == "PATCH":
        field_statement = re.split("=|; ",zahtev_dict["fields"])
        for j in range(len(field_statement)):    
            if(j%2==0 and (field_statement[j] not in fields)):
                return False
    else:
        field_statement = re.split("; ",zahtev_dict["fields"])
        for field in field_statement:
            if field not in fields:
                return False
    
    return True


def provera_formata(zahtev_dict):
    if not (provera_verb(zahtev_dict) and provera_noun(zahtev_dict)):
        return False
    
    # Provera za GET
    if zahtev_dict["verb"] == "GET":
        if "query" in zahtev_dict:
            if not provera_query(zahtev_dict):
                return False
        if "fields" in zahtev_dict:
            if not provera_fields(zahtev_dict):
                return False

    # Provera za DELETE
    if zahtev_dict["verb"] == "DELETE":
        if not provera_query(zahtev_dict):
            return False
    
    # Provera za POST
    if zahtev_dict["verb"] == "POST":
        if not provera_query(zahtev_dict):
            return False
    
    # Provera za PATCH
    if zahtev_dict["verb"] == "PATCH":
        if not provera_query(zahtev_dict):
            return False
        if not provera_fields(zahtev_dict):
            return False
    
    return True
        
if __name__ == "__main__":
    host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_socket.bind((IP, HOST_PORT))
    print("CommunicationBus listening for connections..")
    host_socket.listen()
    conn, addr = host_socket.accept()
    print ('Connection address:', addr)

    xml_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    xml_client_socket.connect((IP, SERVICE_PORT_XMLADAPTER))

    sql_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sql_client_socket.connect((IP, SERVICE_PORT_DATABASE_ADAPTER))

    while True:
        primljeno = conn.recv(BUFFER_SIZE).decode()
        if not primljeno: break
        print ("Received data from webclient:", primljeno)
        zahtev = primljeno
        
        try:
            zahtev_dict=json.loads(zahtev)
        except:
            conn.send('{"odgovor": {"status": "BAD_FORMAT", "statuscode": "5000", "payload": "B A D   F O R M A T"}}'.encode())
            continue
        
        provera=provera_formata(zahtev_dict)
        if provera == True:
            xml_client_socket.send(zahtev.encode())
            XMLzahtev = xml_client_socket.recv(BUFFER_SIZE).decode()
            sql_client_socket.send(XMLzahtev.encode())
            odgovor = sql_client_socket.recv(BUFFER_SIZE).decode()
            xml_client_socket.send(odgovor.encode())
            odgovor = xml_client_socket.recv(BUFFER_SIZE).decode()
            conn.sendall(odgovor.encode())
        else:
            conn.send('{"odgovor": {"status": "BAD_FORMAT", "statuscode": "5000", "payload": "B A D   F O R M A T"}}'.encode())

    host_socket.close()
