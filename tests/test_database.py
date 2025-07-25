import unittest
from src.swen344_db_utils import *
from src.library import rebuildTables
from tests.seed import *

"""
For testing state of swen344 database
"""
class TestDatabase(unittest.TestCase):

    def test_a_rows_of_books(self):
        rebuildTables()
        file = seed_book1()
        count = count_lines_of_info(file)
        result = exec_get_all('SELECT * FROM books')
        if (len(result) > 0):
            self.assertEqual(count, len(result), "books has an incorrect number of rows")
        else:
            self.assertEqual(1, result[0], "books has no information inside")

    def test_b_rows_of_members(self):
        file = seed_member1()
        count = count_lines_of_info(file)
        result = exec_get_all('SELECT * FROM members')
        if (len(result) > 0):
            self.assertEqual(count, len(result), "members has an incorrect number of rows")
        else:
            self.assertEqual(1, result[0], "members has no information inside")

    def test_c_adding_rows_members(self):
        count = exec_get_all('SELECT * FROM members')
        seed_member2()
        result = exec_get_all('SELECT * FROM members')
        if (len(result) > 0):
            self.assertLess(len(count), len(result), "members has not had rows added")

def count_lines_of_info(path):
    with open(path, 'r') as FILE:
        lines = len(FILE.readlines())
        return lines - 1 # -1 because of first line containing code and not table information