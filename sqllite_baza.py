import sqlite3
from sqlite3 import Error

class baza_podataka:
    def __init__(self):
        path = 'resurs.db'
        con = self.create_connection(path)
        self.execute_query(con,self.create_users_type_table)
        self.execute_query(con,self.create_users_table)
        self.execute_query(con,self.create_relations_type_table)
        self.execute_query(con,self.create_relations_table)
        #self.execute_query(con,self.podaci)

    def create_connection(self,path):
        connection = None
        try:
            connection = sqlite3.connect(path)
            print("Connection to SQLite DB successful")
        except Error as e:
            print(f"The error '{e}' occurred")
        return connection

    def execute_query(self,connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query executed successfully")
            return cursor.fetchall()
        except SyntaxError:
            return "REJECTED"
        except:
            return "BAD FORMAT"

    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    description TEXT,
    type INTEGER NOT NULL,
    FOREIGN KEY (type) REFERENCES user_type (id) 
    );
    """
    
    create_users_type_table = """
    CREATE TABLE IF NOT EXISTS user_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
    );
    """

    create_relations_table = """
    CREATE TABLE IF NOT EXISTS relations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idFirstUser INTEGER NOT NULL references users(id),
    idSecondUser  INTEGER NOT NULL references users(id),
    type INTEGER NOT NULL,
    FOREIGN KEY (type) REFERENCES relation_type (id) 
    );
    """

    create_relations_type_table = """
    CREATE TABLE IF NOT EXISTS relation_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT
    );
    """


    #podaci = '''INSERT INTO relations (idFirstUser,idSecondUser,type) VALUES (1,2,2);'''