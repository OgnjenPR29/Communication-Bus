from select import select
import socket
import xml.etree.ElementTree as ET

IP = "127.0.0.1"
HOST_PORT = 5007
SERVICE_PORT = 5008
BUFFER_SIZE = 2048

host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_socket.bind((IP, HOST_PORT))
print("XmlDataBaseAdapter listening for connections..")

# na osnovu zahteva(GET,POST,DELET ili PATCH) bira koju metodu poziva
def to_sql(zahtev):
    verb = zahtev.split("verb")
    verb = verb[1][1:-2]
    get = "GET"
    post = "POST"
    delete = "DELETE"       

    if verb in get:
        return method_get_to_sql(zahtev)
    elif verb in delete:
        return  method_delete_to_sql(zahtev)
    elif verb in post:
        return  method_post_to_sql(zahtev)
    else:
        return method_patch_to_sql(zahtev)

zahtev =""

#vraca ceo query u obliku: name='pera' AND type=1....
def get_query(zahtev):
    if("query" in zahtev):
        query = zahtev.split("query")
        query = query[1][1:len(query[1])-2]
        query = query.replace(";"," AND ")
        return query
    else:
        return False

#vraca samo vredosti iz query-ja('pera' 1 ...)
def get_values_from_query(zahtev):
    query = zahtev.split("query")
    query = query[1][1:len(query[1])-2]
    value = query.split(";")
    
    values = list()
    for i in range(len(value)):
        temp = value[i].split("=")
        values.append(temp[1])
    
    
    return values

def get_names_from_query(zahtev):
    query = zahtev.split("query")
    query = query[1][1:len(query[1])-2]
    value = query.split(";")
    
    values = list()
    for i in range(len(value)):
        temp = value[i].split("=")
        values.append(temp[0])
    

    return values
#vraca polja u obliku: id, name, surname....
def get_fields(zahtev):
    if("fields" in zahtev):
        fields = zahtev.split("fields")
        fields = fields[1][1:len(fields[1])-2]
        fields = fields.replace(";",",")
        return fields

#sluzi samo za PATCH jer vraca polja sa vrednostima za upload(name='pera', type=1...)
def get_fields_with_values(zahtev):
    fields = zahtev.split("fields")
    fields = fields[1][1:len(fields[1])-2]
    fields = fields.replace(";",",")
    return fields

#iz zahteva dobavlja broj tabele
def get_number_table(zahtev):
    if("noun" in zahtev):
        noun = zahtev.split("noun")
        noun = noun[1].split("/")
        noun = noun[2][:-1]
        return int(noun)

#na osnovu broja tabele vraca naziv tabele
def get_string_table(number):
    switcher = {
        1:"users",
        2:"user_type", 
        3:"relations",
        4:"relation_type"
    }
    return switcher.get(number,"n")

#pretvara GET zahtev u sql upit
def method_get_to_sql(zahtev):
    sqlreq = "SELECT "
    if(get_fields(zahtev)):
        sqlreq +=  get_fields(zahtev)+" FROM "
    else:
        sqlreq += "* FROM "
    sqlreq +=  get_string_table(get_number_table(zahtev))
    if(get_query(zahtev)):
        sqlreq += " WHERE "+ get_query(zahtev)
    else:
        return sqlreq
    return sqlreq

#pretvara DELETE zahtev u sql upit
def method_delete_to_sql(zahtev):
    sqlreq = "DELETE FROM "+ get_string_table(get_number_table(zahtev))
    if(get_query(zahtev)):
        sqlreq += " WHERE "+  get_query(zahtev)
    else:
        return sqlreq
    return sqlreq

#pretvara POST zahtev u sql upit
def method_post_to_sql(zahtev):
    cnt = 0
    sqlreq = "INSERT INTO " + get_string_table(get_number_table(zahtev))
    
    sqlreq += "("
    for value in  get_names_from_query(zahtev):
        sqlreq+=value
        cnt +=1
        if cnt == len(get_names_from_query(zahtev)):
            break
        sqlreq += ", "
    sqlreq += ") VALUES("
    
    cnt = 0
    for value in  get_values_from_query(zahtev):
        cnt +=1
        sqlreq += value
        if cnt == len(get_values_from_query(zahtev)):
            break
        sqlreq += ", "
    sqlreq += ")"
    return sqlreq

#pretvara PATCH zahtev u sql upit
def method_patch_to_sql(zahtev):
    sqlreq = "UPDATE "+ get_string_table(get_number_table(zahtev))+ " SET "
    sqlreq +=  get_fields_with_values(zahtev)
    if  get_query(zahtev):
        sqlreq += " WHERE " +  get_query(zahtev)
    return sqlreq

def to_xml(query, result):
    xmlodgrejected = "<odgovor><status>REJECTED</status><statuscode>3000</statuscode><payload>"
    xmlodgrejected = xmlodgrejected  + result + "</payload></odgovor>"

    xmlodgbadformat = "<odgovor><status>BAD_FORMAT</status><statuscode>5000</statuscode><payload>"
    xmlodgbadformat = xmlodgbadformat  + result + "</payload></odgovor>"

    if result == "R E J E C T E D":
        return xmlodgrejected
    if result == "B A D   F O R M A T":
        return xmlodgbadformat

    xmlodgsuccess = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode>"

    if "SELECT" in query:
        if result == "EMPTY":
            pyl="NO SUCH RESOURCE"
        else:
            odg = result.split(" ")  # od stringa koji je dosao iz repository se pravi lista
            pyl = to_payload_select(odg, query)  # ovde se dobija payload

    elif "DELETE" in query:
        pyl = "SUCCESSFULLY DELETED"

    elif "INSERT INTO" in query:
        pyl = "SUCCESSFULLY INSERTED"

    elif "UPDATE" in query:
        pyl = "SUCCESSFULLY UPDATED"

    payload = "<payload>"+pyl+"</payload>"

    rez = xmlodgsuccess + payload + "</odgovor>"

    return rez

def to_payload_select(result, query):

    payload = ""

    start = query.find('SELECT') + 7
    end = query.find(' FROM', start)
    pom = query[start:end]

    if "*" in pom:
        if "FROM users" in query:
            pom = "id, name, surname, description, type"
        elif "FROM user_type" in query:
            pom = "id, title"
        elif "FROM relations" in query:
            pom = "id, idFirstUser, idSecondUser, type"
        elif "FROM relation_type" in query:
            pom = "id, title"

    fields = pom.split(","+" ") #niz polja koja se kupe iz baze

    duzina = len(fields)#koliko ima clanova niz fielda
    j = 0

    #u ovim petljama se pravi payload tj xml odgovor iz baze
    while j<len(result):
        i=0
        payload = payload + '<resurs>'
        while i < duzina:
            payload = payload + '<' + fields[i] + '>' + result[j] + '</' + fields[i] + '>'
            j = j+1
            i = i+1
        payload = payload + "</resurs>"
    return payload

if __name__ == "__main__":

    host_socket.listen()

    conn, addr = host_socket.accept()
    print ('Connection address:', addr)

    repository_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    repository_client_socket.connect((IP, SERVICE_PORT))

    while True:
        primljeno = conn.recv(BUFFER_SIZE).decode()
        if not primljeno: break
        print ("Received data from client:", primljeno)
        zahtev = primljeno
        
        zahtev = to_sql(zahtev)
        repository_client_socket.send(zahtev.encode())
        odgovor = repository_client_socket.recv(BUFFER_SIZE).decode()
        conn.sendall(to_xml(zahtev,odgovor).encode())
        print(odgovor)