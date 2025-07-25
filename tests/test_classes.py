import unittest
import datetime
from src.classes import *
from src.library import rebuildTables
from tests.seed import seed_book1, seed_member1, seed_member2

"""Filled with tests for classes.py"""
"""Will fill later"""
class TestClass(unittest.TestCase):
    
    def test_a_books_tup(self):
        rebuildTables()
        seed_book1()
        wrapper = books((1, 'Fahrenheit 451', 'Ray Bradbury', datetime.date(1953, 10, 19), '978-1451673319', 'Fiction', 'Science Fiction', 'im a text, short and stout', 10, 1, 0))
        self.assertEqual(str(wrapper.tup),"(1, 'Fahrenheit 451', 'Ray Bradbury', datetime.date(1953, 10, 19), '978-1451673319', 'Fiction', 'Science Fiction', 'im a text, short and stout', 10, 1, 0)")

    def test_b_books_map(self):
        wrapper = books((1, 'Fahrenheit 451', 'Ray Bradbury', datetime.date(1953, 10, 19), '978-1451673319', 'Fiction', 'Science Fiction', 'im a text, short and stout', 10, 1, 0))
        self.assertEqual(wrapper.map["books_id"], 1)

    def test_c_members_tup(self):
        seed_member1()
        seed_member2()
        wrapper = members((1, 'WonderfulNeighbor', 'Mr.', 'Rogers', 'mr@gmail.com', '1234567890', '', 0, True))
        self.assertEqual(wrapper.tup, (1, 'WonderfulNeighbor', 'Mr.', 'Rogers', 'mr@gmail.com', '1234567890', '', 0, True))
        
    def test_d_members_map(self):
        wrapper = members((1, 'WonderfulNeighbor', 'Mr.', 'Rogers', 'mr@gmail.com', '1234567890', '', 0, True))
        self.assertEqual(wrapper.map["members_id"], 1)