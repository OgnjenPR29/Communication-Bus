import sys
sys.path.append("..")
import unittest
from CommunicationBus import provera_formata

class testformat(unittest.TestCase):
    def test1(self):
        primer = {
            "verb": "GET",
            "noun": "/resurs/1",
            "query": "name='pera'", 
            "fields": "id; name; surname" 
            }
        
        self.assertTrue(provera_formata(primer))
    def test2(self):
        primer = {
            "verb": "DELETE",
		    "noun": "/resurs/1",
		    "query": "id=1"
            }
        self.assertTrue(provera_formata(primer))
    def test3(self):
        primer = {
            "verb": "POST",
		    "noun": "/resurs/1",
		    "query": "name='mika'; surname='mikic'; type=1"
            }
        self.assertTrue(provera_formata(primer))
    def test4(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "query": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertTrue(provera_formata(primer))
    def test5(self):
        primer = {
            "": "PATCH",
		    "noun": "/resurs/1",
		    "query": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test6(self):
        primer = {
            "verb": "PATCH",
		    "": "/resurs/1",
		    "query": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test7(self):
        primer = {
            "verb": "",
		    "noun": "/resurs/1",
		    "query": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test8(self):
        primer = {
            "verb": "PATCH",
		    "noun": "",
		    "query": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test9(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "": "name='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test10(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "query": "name='mika'; type=1",
		    "": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test11(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "query": "nme='mika'; type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test12(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "query": "name='mika' type=1",
		    "fields": "name='zika'"
            }
        self.assertFalse(provera_formata(primer))
    def test13(self):
        primer = {
            "verb": "PATCH",
		    "noun": "/resurs/1",
		    "query": "name='mika'; type=1",
		    
            }
        self.assertFalse(provera_formata(primer))
    def test14(self):
        primer = {
            "verb": "DELETE",
		    "noun": "/resurs/1",
		    
            }
        self.assertFalse(provera_formata(primer))
    def test15(self):
        primer = {
            "verb": "POST",
		    "noun": "/resurs/1",

            }
        self.assertFalse(provera_formata(primer))
    def test16(self):
        primer = {
            "verb": "GET",
		    "noun": "/resurs/1",

            }
        self.assertTrue(provera_formata(primer))
if __name__ == "__main__":
    unittest.main()