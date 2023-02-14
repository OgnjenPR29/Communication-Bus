import sys
sys.path.append("..")
import unittest
from JsonToXmlAdapter import json_to_xml
from JsonToXmlAdapter import xml_to_json


class testadapter(unittest.TestCase):

    def test1(self):

        primer = '{"verb": "GET", "noun": "/resurs/1", "query": "name=\'koja\'", "fields": "id; name; surname"}'
        ispis = '''b"<?xml version='1.0' encoding='utf8'?>\\n<request><verb>GET</verb><noun>/re'''
        ispis = ispis + '''surs/1</noun><query>name='koja'</query><fields>id; name; surname</fields></r'''
        ispis = ispis+ '''equest>"'''

        self.assertMultiLineEqual(json_to_xml(primer), ispis)


    def test_delete(self):

        primer = "{\"verb\": \"DELETE\", \"noun\": \"/resurs/1\", \"query\": \"id=1\"}"

        ispis2 = '''b"<?xml version='1.0' encoding='utf8'?>\\n<request><verb>DELETE</verb><noun>'''
        ispis2 = ispis2 + '''/resurs/1</noun><query>id=1</query></request>"'''

        self.assertEqual(json_to_xml(primer), ispis2)

    def test_patch(self):

        primer = '{"verb": "PATCH", "noun": "/resurs/1", "query": "name=\'mika\'; type=1", "fields": "name=\'zika\'"}'

        ispis2 = '''b"<?xml version='1.0' encoding='utf8'?>\\n<request><verb>PATCH</verb><noun>/resurs/1</noun>'''
        ispis = ispis2 + '''<query>name='mika'; type=1</query><fields>name='zika'</fields></request>"'''

        self.assertEqual(json_to_xml(primer), ispis)

    def test_post(self):

        primer = '{"verb": "POST", "noun": "/resurs/1", "query": "name=\'mika\'; surname = \'mikic\'; type=1"}'

        ispis2 = '''b"<?xml version='1.0' encoding='utf8'?>\\n<request><verb>POST</verb><noun>/resurs/1</noun>'''
        ispis = ispis2 + '''<query>name='mika'; surname = 'mikic'; type=1</query></request>"'''

        self.assertEqual(json_to_xml(primer), ispis)

    def test_xml_to_json(self):

        primer = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>NO SUCH "
        primer = primer + "RESOURCE</payload></odgovor>"
        ispis = '''{"odgovor": {"status": "SUCCESS", "statuscode": "2000", "payload": "NO SUCH RESOURCE"}}'''
        self.assertEqual(xml_to_json(primer), ispis)

    def test_xml_to_json2(self):

        primer = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload>SUCCESSFULLY "
        primer = primer + "DELETED</payload></odgovor>"
        ispis = '''{"odgovor": {"status": "SUCCESS", "statuscode": "2000", "payload": "SUCCESSFULLY DELETED"}}'''
        self.assertEqual(xml_to_json(primer), ispis)

    def test_xml_to_json3(self):

        primer = "<odgovor><status>BAD FORMAT</status><statuscode>5000</statuscode><payload>B A D   F O R M A T"
        primer = primer + "</payload></odgovor>"
        ispis = '''{"odgovor": {"status": "BAD FORMAT", "statuscode": "5000", "payload": "B A D   F O R M A T"}}'''
        self.assertEqual(xml_to_json(primer), ispis)

    def test_xml_to_json4(self):

        primer = "<odgovor><status>REJECTED</status><statuscode>3000</statuscode><payload>R E J E C T E D"
        primer = primer + "</payload></odgovor>"
        ispis = '''{"odgovor": {"status": "REJECTED", "statuscode": "3000", "payload": "R E J E C T E D"}}'''
        self.assertEqual(xml_to_json(primer), ispis)

    def test_xml_to_json5(self):

        primer = "<odgovor><status>SUCCESS</status><statuscode>2000</statuscode><payload><resurs>"
        primer = primer + "<name>pera</name></resurs></payload></odgovor>"
        ispis = '''{"odgovor": {"status": "SUCCESS", "statuscode": "2000", "payload": {"resurs": {"name": "pera"}}}}'''
        self.assertEqual(xml_to_json(primer), ispis)

if __name__ == "__main__":
    unittest.main()
