import sys
sys.path.append("..")
import unittest
from XmlDataBaseAdapter import to_sql
from XmlDataBaseAdapter import to_xml
from XmlDataBaseAdapter import to_payload_select


class test_xml_data_base_adapter(unittest.TestCase):
    def test_get(self):
        zahtev1="<request><verb>GET</verb><noun>/resurs/1</noun><query>name='pera';type=1</query><fields>id; name; surname</fields></request>"
        self.assertEqual(to_sql(zahtev1) , "SELECT id, name, surname FROM users WHERE name='pera' AND type=1")

    def test_delete(self):
        zahtev1="<request><verb>DELETE</verb><noun>/resurs/1</noun><query>name='pera';type=1</query></request>"
        self.assertEqual(to_sql(zahtev1) , "DELETE FROM users WHERE name='pera' AND type=1")
   
   
    def test_patch(self):
        zahtev1="<request><verb>PATCH</verb><noun>/resurs/1</noun><query>name='pera';type=1</query><fields>id=2; name='zika'; surname='maric'</fields></request>"
        self.assertEqual(to_sql(zahtev1) , "UPDATE users SET id=2, name='zika', surname='maric' WHERE name='pera' AND type=1")
   
   
    def test_post(self):
        zahtev1="<request><verb>POST</verb><noun>/resurs/1</noun><query>name='pera';type=1</query></request>"
        self.assertEqual(to_sql(zahtev1) , "INSERT INTO users(name, type) VALUES('pera', 1)")

    def test_get_all(self):
        zahtev1="<request><verb>GET</verb><noun>/resurs/1</noun></request>"
        self.assertEqual(to_sql(zahtev1) , "SELECT * FROM users")

    def test_delete_all(self):
        zahtev1="<request><verb>DELETE</verb><noun>/resurs/1</noun></request>"
        self.assertEqual(to_sql(zahtev1) , "DELETE FROM users")

    def test_to_xml_rej(self):

        ispis = "<odgovor><status>REJECTED</status><statuscode>3000</statuscode><payload>R E J E C T E D</payload></odgovor>"
        

        zahtev = "SELECT * FROM nepostojeca"
        odgovor = "R E J E C T E D"
        
        self.assertEqual(to_xml(zahtev, odgovor), ispis)
        
    def test_to_xml_bf(self):

        ispis = "<odgovor><status>BAD_FORMAT</status><statuscode>5000</statuscode><payload>"
        ispis = ispis + "B A D   F O R M A T</payload></odgovor>"

        zahtev = "SELECT FROM users"
        odgovor = "B A D   F O R M A T"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_xml_succ(self):

        ispis = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>"
        ispis = ispis + "<resurs><id>1</id><name>pera</name><surname>peric</surname></resurs>"
        ispis = ispis + "<resurs><id>2</id><name>pera</name><surname>mikic</surname></resurs></payload></odgovor>"

        zahtev = "SELECT id, name, surname FROM users WHERE name='pera'"
        odgovor = "1 pera peric 2 pera mikic"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_xml_succ_del(self):

        ispis = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>"
        ispis = ispis + "SUCCESSFULLY DELETED</payload></odgovor>"

        zahtev = "DELETE FROM users WHERE name='pera' AND type=1"
        odgovor = "EMPTY"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_xml_succ_up(self):

        ispis = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>"
        ispis = ispis + "SUCCESSFULLY UPDATED</payload></odgovor>"

        zahtev = "UPDATE users SET id=2, name='zika', surname='maric' WHERE name='pera' AND type=1"
        odgovor = "EMPTY"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_xml_succ_add(self):
        ispis = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>"
        ispis = ispis + "SUCCESSFULLY INSERTED</payload></odgovor>"

        zahtev = "INSERT INTO users(name, type) VALUES('pera', 1)"
        odgovor = "EMPTY"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_xml_no_select(self):
        ispis = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>"
        ispis = ispis + "NO SUCH RESOURCE</payload></odgovor>"

        zahtev = "SELECT id, name, surname FROM users WHERE name='pera'"
        odgovor = "EMPTY"
        self.assertEqual(to_xml(zahtev, odgovor), ispis)

    def test_to_payload_select_all1(self):

        ispis = "<resurs><id>1</id><name>pera</name><surname>peric</surname><description>opis</description>"
        ispis= ispis + "<type>1</type></resurs>"

        zahtev = "SELECT * FROM users WHERE name='pera'"
        odgovor =  ["1", "pera", "peric", "opis", "1"]
        self.assertEqual(to_payload_select(odgovor, zahtev), ispis)

    def test_to_payload_select_all2(self):

        ispis = "<resurs><id>1</id><title>musko</title></resurs>"

        zahtev = "SELECT * FROM user_type WHERE id=1"
        odgovor = ["1", "musko"]
        self.assertEqual(to_payload_select(odgovor, zahtev), ispis)

    def test_to_payload_select_all3(self):

        ispis = "<resurs><id>1</id><idFirstUser>2</idFirstUser><idSecondUser>1</idSecondUser><type>3</type></resurs>"

        zahtev = "SELECT * FROM relations WHERE id=1"
        odgovor = ["1", "2", "1", "3"]
        self.assertEqual(to_payload_select(odgovor, zahtev), ispis)

    def test_to_payload_select_all4(self):

        ispis = "<resurs><id>1</id><title>rodbina</title></resurs>"

        zahtev = "SELECT * FROM relation_type WHERE id=2"
        odgovor = ["1", "rodbina"]
        self.assertEqual(to_payload_select(odgovor, zahtev), ispis)

    def test_to_payload_select_regular(self):

        zahtev = "SELECT id, name FROM users WHERE type=2"
        odgovor = ["1","maja", "2", "ivana"]

        ispis = "<resurs><id>1</id><name>maja</name></resurs><resurs><id>2</id><name>ivana</name></resurs>"

        self.assertEqual(to_payload_select(odgovor, zahtev), ispis)


if __name__ == "__main__":
    unittest.main()