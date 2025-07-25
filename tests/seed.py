from src.swen344_db_utils import *

DIR_PATH = os.path.join(os.path.dirname(__file__), 'testdata/')
str_DIR_PATH = 'tests/testdata/'

def seed_book1():
    """
    Inserts first set of seed data for books into database.
    
    Returns file path
    """
    
    file = str_DIR_PATH + "bookdata1.sql"
    exec_sql_file(file)
    return file

def seed_member1():
    """
    Inserts first set of seed data for members into database.
    
    Returns file path
    """

    file = str_DIR_PATH + "memberdata1.sql"
    exec_sql_file(file)
    return file

def seed_member2():
    """
    Inserts second set of seed data for members into database.
    
    Returns file path
    """

    file = str_DIR_PATH + "memberdata2.sql"
    exec_sql_file(file)
    return file

def seed_inventory1():
    """
    Inserts first set of seed data for inventory into database.
    
    Returns file path
    """

    file = str_DIR_PATH + "invdata1.sql"
    exec_sql_file(file)
    return file

def seed_history1():
    """
    Inserts first set of seed data for history into database.
    
    Returns file path
    """

    file = str_DIR_PATH + "histdata1.sql"
    exec_sql_file(file)
    return file