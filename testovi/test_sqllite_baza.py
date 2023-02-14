import sys
sys.path.append("..")
import unittest
from sqllite_baza import baza_podataka

class test_sqllite_baza(unittest.TestCase):
    def test1(self):
        zahtev = "SELECT FROM users"
        baza = baza_podataka()
        path = 'resurs.db'
        con = baza.create_connection(path)
        self.assertEqual(baza.execute_query(con,zahtev),"BAD FORMAT")
        

if __name__ == "__main__":
    unittest.main()