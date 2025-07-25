import sys
from src import *

def str_to_class(classname: str): # source: https://stackoverflow.com/a/1176180
    return getattr(sys.modules[__name__], classname)

def mapBuilder(c: tuple[str], b: tuple[any]) -> dict[str: any]:
    """force construction of a map slowly"""
    mapped = {}
    for i in range(len(c)):
        mapped[c[i]] = b[i]
    return mapped

class books:
    """wrapper class for a books row"""
    def __init__(self, book: tuple[any]):
        cols = None
        if not COLUMNS.keys().__contains__("books"):
            cols = columns_by_table()
        else:
            cols = COLUMNS
        self.map = mapBuilder(cols["books"], book) 
        self.tup = book

class members:
    """wrapper class for a members row"""
    def __init__(self, member: tuple[any]):
        cols = None
        if not COLUMNS.keys().__contains__("members"):
            cols = columns_by_table()
        else:
            cols = COLUMNS
        self.map = mapBuilder(cols["members"], member) 
        self.tup = member

class inventory:
    """wrapper class for an inventory row"""
    def __init__(self, inventory: tuple[any]):
        cols = None
        if not COLUMNS.keys().__contains__("inventory"):
            cols = columns_by_table()
        else:
            cols = COLUMNS
        self.map = mapBuilder(cols["inventory"], inventory) 
        self.tup = inventory

class history:
    """wrapper class for a history row"""
    def __init__(self, history: tuple[any]):
        cols = None
        if not COLUMNS.keys().__contains__("history"):
            cols = columns_by_table()
        else:
            cols = COLUMNS
        self.map = mapBuilder(cols["history"], history) 
        self.tup = history