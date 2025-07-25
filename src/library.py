import csv
import datetime
from src import LIBRARIES
from src.swen344_db_utils import *
from src.classes import books, members, inventory, history, mapBuilder

def add_wrapper_to_iter(it: any, cl: any) -> tuple:
    """
    Helper function that takes an iterable and makes its contents into a tuple of wrappers
    
    it: is any iterable that is not a dictionary filled with unwrapped information from a table
    cl: is one of the wrapper classes

    returns a tuple of wrappers
    """

    li = []
    for unwrapped in it:
        li.append(cl(unwrapped))
    return tuple(li)

def rebuildTables():
    """Restarts the entire schema"""
    exec_sql_file("src/LibrarySchema.sql")

def book_lookup_i(isbn: str) -> books:
    """Looks up a row in members based on the isbn"""
    try:
        return books(exec_get_one("SELECT * FROM books WHERE books.isbn = %s", (isbn,)))
    except:
        return None

def book_lookup_t(title: str) -> tuple[books]:
    """Looks up all rows in members based on the title"""
    try:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM books WHERE books.title = %s", (title,)), books)
    except:
        return None
    
def book_lookup_a(author: str) -> tuple[books]:
    """Looks up all rows in members based on the author"""
    try:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM books WHERE books.author = %s", (author,)), books)
    except:
        return None 

def book_lookup(id: int) -> books:
    """Looks up a row in books based on the id"""
    try:
        return books(exec_get_one("SELECT * FROM books WHERE books.books_id = %s", (str(id),)))
    except:
        return None

def member_lookup(id: int) -> members:
    """Looks up a row in members based on the id"""
    try:
        return members(exec_get_one("SELECT * FROM members WHERE members.members_id = %s", (str(id),)))
    except:
        return None

def member_lookup_phone(phonenumber: str) -> members:
    """Looks up a row in members based on the phonenumber"""
    try:
        return members(exec_get_one("SELECT * FROM members WHERE members.phonenumber = %s", (phonenumber,)))
    except:
        return None

def member_lookup_email(email: str) -> members:
    """Looks up a row in members based on the email"""
    try:
        return members(exec_get_one("SELECT * FROM members WHERE members.email = %s", (email,)))
    except:
        return None

def inv_lookup_m(id: members, library: str = "") -> tuple[inventory]:
    """Looks up as many rows as the member id matches in inventory"""
    if library == "":
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.lent_to = %s;", (str(id.map["members_id"]),)), inventory)
    else:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.lent_to = %s AND inventory.library = %s;", (str(id.map["members_id"]), library)), inventory)

def inv_lookup_b(id: books, library: str = "", mustBeLended: bool = False) -> tuple[inventory]:
    """Looks up as many rows as the book_id matches in inventory"""
    if library == "":
        if mustBeLended:
            return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.books_id = %s AND inventory.lent_to != 0 ORDER BY lent_to DESC;", (str(id.map["books_id"]),)), inventory)
        else:
            return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.books_id = %s ORDER BY lent_to DESC;", (str(id.map["books_id"]),)), inventory)
    else:
        if mustBeLended:
            return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.books_id = %s AND inventory.library = %s AND inventory.lent_to != 0 ORDER BY lent_to DESC;", (str(id.map["books_id"]), library)), inventory)
        else:
            return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.books_id = %s AND inventory.library = %s ORDER BY lent_to DESC;", (str(id.map["books_id"]), library)), inventory)

def inv_lookup(id: int, library = "") -> inventory:
    """Looks up a row in inventory based on the inventory_id"""
    try:
        if library == "":
            return inventory(exec_get_one("SELECT * FROM inventory WHERE inventory.inventory_id = %s;", (str(id),)))
        else:
            return inventory(exec_get_one("SELECT * FROM inventory WHERE inventory.inventory_id = %s AND inventory.library = %s;", (str(id), library))) 
    except:
        return None
    
def hist_dates(id: int) -> dict:
    """
    gets a dictionary of the lent date and the date due
    
    returns Dict("date_lent" | "date_due" : Datetime.date)
    """

    di = dict()
    values = exec_get_one("SELECT date_lent, date_due FROM history WHERE history.history_id = %s;", (str(id),))
    keys = ("date_lent", "date_due")
    for i in range(2):
        di[keys[i]] = values[i]
    return di

def history_lookup(id: int):
    """Gets a row of history and returns a wrapper of it"""
    try:
        return history(exec_get_one("SELECT * FROM history WHERE history.history_id = %s", (str(id),)))
    except:
        return None
    
def history_lookup_member(id: int):
    """Gets all rows of history that equal a members id"""
    try:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM history WHERE history.members_id = %s", (str(id),)))
    except:
        return None
    
def history_lookup_books(id: int):
    """Gets all rows of history that equal a books id"""
    try:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM history WHERE history.books_id = %s", (str(id),)))
    except:
        return None
    
def history_lookup_inventory(id: int):
    """Gets all rows of history that equal a inventory id"""
    try:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM history WHERE history.inventory_id = %s", (str(id),)))
    except:
        return None
    
def history_lookup_member_book(member: members, book: books, get_all: bool = False):
    """
    Gets a histories based off of the member and book.
    
    get_all: bool that differentiates between the most recent(False) and all books(True)
    """
    
    b_id = book.map["books_id"]
    m_id = member.map["members_id"]
    try:
        if get_all:
            return add_wrapper_to_iter(exec_get_all("SELECT * FROM history WHERE history.members_id = %s AND history.books_id = %s", (m_id, b_id)), history)
        else:
            return history(exec_get_one("SELECT * FROM history WHERE history.members_id = %s AND history.books_id = %s", (m_id, b_id)))
    except:
        return None
    
def history_to_string(hist: history) -> str:
    """returns the given history as a string"""
    title = book_lookup(hist.map["books_id"]).map["title"]
    member = member_lookup(hist.map["members_id"])
    fname = member.map["first_name"]
    lname = member.map["last_name"]

    returned = hist.map["date_returned"]
    if returned == None:
        returned = " not returned yet"
    else:
        returned = " and returned on " + str(returned)
    return "" + fname + " " + lname + ": Checked out " + title + " on " + str(hist.map["date_lent"]) + " due on " + str(hist.map["date_due"]) + returned

def is_active(member_id: int):
    """Gets if a member is active"""
    tup = exec_get_one("SELECT members_id, active FROM members WHERE members.members_id = %s;", (str(member_id), ))
    return tup[1]

def is_valid_library(library: str) -> bool:
    """helper function to determine if a library name is valid"""
    return library in LIBRARIES

def has_overdue(member_id: int, date: datetime.date = datetime.date.today()):
    """
    Checks if a member has overdue books
    
    member_id: a member's id
    date: **TESTING ONLY** date using datetime module. Defaults to today 
    """
    
    historys = exec_get_all("SELECT * FROM history WHERE history.members_id = %s AND history.date_due < %s", (member_id, str(date)))
    return len(historys) > 0

def book_checkout(member: members, book: books, library: str, date: datetime.date = datetime.date.today()) -> int:
    """
    Check out a book by inputing a member and a book. Stops checkout if its found they have an overdue book

    members: a members wrapper
    book: a books wrapper
    library: one of the valid library names

    Returns a status code: -1 for overdue book, 0 for checked out, 1 for failure, 2 for reserved 
    """

    if not is_active(member.map["members_id"]):
        return 1 #inactive
    if not is_valid_library(library):
        return 1
    if len(inv_lookup_b(book, library)) == 0:
        return 1 #see if this library has this book
    if has_overdue(member.map["members_id"], date):
        return -1 #overdue

    inv_tup = get_checked_out(member.map["members_id"], asBooks=False) 
    for inv in inv_tup:
        if inv.map["books_id"] == book.map["books_id"]:
            return 1 #the same member already has this book checked out, so fail

    if book.map["lended"] < book.map["in_stock"]:
        exec_commit("UPDATE books SET lended={0!s} WHERE books.books_id = {1!s};".format(str(book.map.get("lended") + 1), book.map.get("books_id")))
        inv = inventory(exec_get_one("SELECT * FROM inventory WHERE inventory.books_id = {0!s} AND inventory.lent_to = 0;".format(str(book.map["books_id"]))))
        inv_id = str(inv.map["inventory_id"])
        hist_id = create_history((inv_id, book.map["books_id"], member.map["members_id"]), date, date + datetime.timedelta(weeks=2))
        exec_commit("UPDATE inventory SET lent_to=%s, history_id=%s WHERE inventory.inventory_id = %s;", (str(member.map["members_id"]), str(hist_id), str(inv_id)))
        return 0 #checked out
    elif book.map["reserved"] != 0: # book is already reserved
        return 1 #reserved not available
    else:
        book_tup = exec_get_all("SELECT books_id, books.reserved FROM books INNER JOIN members ON books.reserved = members.members_id;")
        alreadyReserved = False
        for book in book_tup:
            if book[1] == member.map["reserved"]:
                alreadyReserved = True
        if alreadyReserved:
            return 1
        exec_commit("UPDATE books SET reserved=%s WHERE books.books_id = %s;", (member.map["members_id"], book.map["books_id"]))
        exec_commit("UPDATE members SET reserved=%s WHERE members.members_id = %s;", (book.map["books_id"], member.map["members_id"]))
        return 2 #reserved
    
def book_checkout_reserved(member: members, date: datetime.date = datetime.date.today()) -> int:
    """
    Claims the reserved book by the member. Not allowed if they have an overdue book<br>
    Returns a status code: 0 for success, 1 for failure
    """
    if not has_overdue(member.map["members_id"]):
        inv = inventory(exec_get_one("SELECT * FROM inventory WHERE inventory.lent_to = %s AND inventory.books_id = %s;", (str(member.map["members_id"]), str(member.map["reserved"]))))
        if inv != ():
            hist_id = create_history((inv.map["inventory_id"], member.map["reserved"], member.map["members_id"]), date, date + datetime.timedelta(weeks=2))
            exec_commit("UPDATE members SET reserved=0 WHERE members.members_id = %s", (member.map["members_id"],))
            exec_commit("UPDATE inventory SET history_id=%s WHERE inventory.inventory_id = %s", (str(hist_id), str(inv.map["inventory_id"])))
            return 0
    return 1

def book_returned(member: members, books_id: int, date: datetime = datetime.date.today()) -> int:
    """
    Handles book returns

    member: members wrapper. The person returning their book <br>
    books_id: id of the book wanting to be returned <br>
    date: **TESTING ONLY** adjusts the date out in the histories

    returns status code: 0 for success, 1 for failure
    """

    m_id = member.map["members_id"]
    book = book_lookup(books_id)
    poi = exec_get_one("""SELECT * FROM history WHERE history.books_id = %s AND history.members_id = %s AND history.date_returned IS NULL""", (books_id, m_id))

    if poi != None:
        hist = history(poi)
        poi = inv_lookup(hist.map["inventory_id"])
        # make history
        ret_info = add_returned_date(hist, date)
        exec_commit("UPDATE inventory SET history_id = 0 WHERE inventory.inventory_id = %s", (hist.map["inventory_id"], ))
        res = book.map["reserved"]
        if res == 0:
            exec_commit("UPDATE books SET lended=%s WHERE books.books_id = %s;", (str(book.map["lended"] - 1), str(books_id)))     
            exec_commit("UPDATE inventory SET lent_to=%s WHERE inventory.inventory_id = %s;", ("0", str(poi.map["inventory_id"])))
        else:
            exec_commit("UPDATE books SET reserved=0 WHERE books.books_id = %s;", (int(books_id), ))
            exec_commit("UPDATE members SET reserved=0 WHERE members.members_id = %s;", (int(member.map["members_id"]), ))
            exec_commit("UPDATE inventory SET lent_to=%s WHERE inventory.inventory_id = %s;", (str(res), str(poi.map["inventory_id"])))
        if type(ret_info).__name__ != 'tuple':
            return None
        else:
            print("You returned your book "+ str(ret_info[0]) +" days late. You have a late fee of $"+ str(ret_info[1]))
            return ret_info
    return None

def get_checked_out(member_id: int, library: str = "", asBooks = True, asString = False):
    """
    Gets the books checked out by a member.
    
    <b>SETTING asBooks TO FALSE WILL FORCE A RETURN OF TUPLE[INVENTORY]</b>

    member_id: int<br>
    library: str. Only valid library names are allowed, leave empty to ignore<br>
    asBooks defaults true<br>
    asString default false. To change return mode

    returns, a tuple[inventory], a tuple[books], or a string of books

    string = member_id: (title,...)
    """

    if not is_valid_library(library) and not library == "":
        return None

    inv_tup = inv_lookup_m(member_lookup(member_id), library)
    if inv_tup == ():
        return ''
    if not asBooks:
        return inv_tup
    li = list()
    for inv_row in inv_tup:
        li.append(book_lookup(inv_row.map["books_id"]))
    book_tup = tuple(li.copy())
    if asString:
        li.clear()
        for book in book_tup:
            li.append(book.map["title"])
        li.sort()
        string = str(member_id) + ": ("
        first = True
        for title in li:
            if not first:
                string += ", "
            string += title
            first = False
        return string + ")"
    else: 
        return book_tup
  
def get_all_checked_out(library: str = "", returnAsString: bool = False):
    """
    Gets all the checked out books and who they are checked out by

    library: to specify what library to get the information from, defaults empty<br>
    returnAsString: boolean to change return variant

    returns: a dictionary[member_ids: book_ids | tuple[books_id]], string
    """

    inv_id_mem = None
    if library != "":
        inv_id_mem = exec_get_all("""SELECT lent_to, books_id FROM inventory 
                                    INNER JOIN members ON inventory.lent_to = members.members_id
                                    AND inventory.library = %s
                                    ORDER BY lent_to""",  (library, ))
    else:
        inv_id_mem = exec_get_all("""SELECT lent_to, books_id FROM inventory 
                                    INNER JOIN members ON inventory.lent_to = members.members_id
                                    ORDER BY lent_to""")
    di = dict()
    for tup in inv_id_mem:
        if di.keys().__contains__(tup[0]):
            di[tup[0]] = (di[tup[0]],) + (tup[1],)
        else:
            di[tup[0]] = tup[1]
    if not returnAsString:
        return di
    else:
        string= "{{"
        first = True
        for m_id in di.keys():
            if not first:
                string += ', '
            string += "{" + member_lookup(m_id).map["username"] + ": ("
            value = di[m_id]
            if type(value).__name__ == "tuple":
                uno = True
                for val in value:
                    if not uno:
                        string += ", "
                    string += book_lookup(val).map["title"]
                    uno = False
            else:
                string += book_lookup(value).map["title"]
            string += ")}"
            first = False
        return string + "}}"
    
def get_all_not_checked_out() -> tuple[inventory]:
    """Returns all books that are not currently checked out"""
    return add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE lent_to = 0 AND history_id = 0;"), inventory)
    
def get_all_ever_checked_out() -> str:
    """
    Returns a formatted string of every book ever checked out in the library
    
    Formatted as:<br>
    Inventory id, title, history {member_id, date_lent, date_due, date_recieved}, in_stock: int, 
    """
    mishmash = exec_get_all("""  SELECT history.*, books.in_stock FROM history
                                    INNER JOIN books ON history.books_id = books.books_id

                                    ORDER BY genre, REVERSE(SPLIT_PART(REVERSE(TRIM(TRAILING FROM books.author)), ' ', 1)), history.members_id ASC""")
                                                    # trim the end to remove any whitespace, reverse the string to get last names in front,
                                                    # split by spaces and get the first section, then reverse again to correct
    string = "{{\n"
    for tup in mishmash:
        if string != "{{\n":
            string += '\n'
        hist = history(tup[:len(tup) - 1])
        string += "{inv_id: " + str(tup[3]) + ", " + history_to_string(hist) + ", in stock: " + str(tup[8]) + "}"
    string += "\n}}"
    return string

def report_all_ever_checked_out() -> str:
    """Returns a formatted string of analytics data for every book ever checked out"""
    space = 4
    all_tups = exec_get_all("""SELECT books.title, members.first_name || ' ' ||  members.last_name, history.date_lent, history.date_returned
                                    FROM history
                                    INNER JOIN books ON history.books_id = books.books_id
                                    INNER JOIN members ON history.members_id = members.members_id
                                    ORDER BY history.inventory_id""")
    headers = ("Title", "User", "Checkout", "Returned")
    infos = list([headers,] + list(all_tups))
    lengths = [0, 0, 0, 0]
    leng = 0
    longest = 0
    for j in range(len(infos[0])):
        longest = 0
        for i in range(len(infos)):
            longest = lengths[j]
            item = infos[i][j]
            if type(item).__name__ != "str":
                leng = len(str(item))
            else:
                leng = len(item)
            if longest < leng + space:
                lengths[j] = leng + space

    
    tab_of_str = list()
    days_late = list()
    for i in range(len(infos)):
        string = ""
        if string != "":
            string += '\n'
        for j in range(len(infos[i])):
            item = infos[i][j]
            if type(item).__name__ != "str":
                item = str(item)
            leng = lengths[j] - len(item)
            white = _build_whitespace(leng)
            string += item + white
        if infos[i][3] == "Returned":
            string += "Days Borrowed"
        else:
            if infos[i][3] != None:
                calc = (infos[i][3] - infos[i][2]).days
                string += str(calc)
                days_late.append(calc)
            else:
                string += "None"
        tab_of_str.append(string)
    
    string = ""
    for row in tab_of_str:
        if string != "":
            string += '\n'
        string += row
    
    sum = 0
    for num in days_late:
        sum += sum + num
    avg = int(sum / len(days_late))
    string += "\n\nAverage return time = " + str(avg) + " days"

    return string

def get_report_all() -> str:
    """String of all books at all libraries, organized by library"""
    string = ""
    for lib in LIBRARIES:
        if string != "":
            string += "\n"
        string += lib + ":\n"
        # returns in order by title for the library a tuple of (<book_id>, <title>)
        tuppd = exec_get_all("""SELECT DISTINCT(books.books_id), title FROM books
                                    INNER JOIN inventory ON books.books_id = inventory.books_id
                                    WHERE library = %s
                                    ORDER BY title""", (lib,))
        # returns the count of books that are in stock at a give library
        books_in_libr = exec_get_all("""SELECT COUNT(in_stock) FROM books
                                            INNER JOIN inventory ON books.books_id = inventory.books_id
                                            WHERE library = %s
                                            GROUP BY books.books_id
                                            ORDER BY title""", (lib,))
        sub = ""
        for i in range(len(tuppd)):
            tup = tuppd[i]
            copies = str(books_in_libr[i][0])
            if sub != "":
                sub += "\n"
            sub += "\t(" + tup[1] + ", copies: " + copies + ")"
        string += sub
    return string

def get_all_members(includeInactive = False) -> tuple[members]:
    """Returns a tuple of all wrapped members in the database"""
    if not includeInactive:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM members WHERE members.active = TRUE;"), members)
    else:
        return add_wrapper_to_iter(exec_get_all("SELECT * FROM members;"), members)

def get_all_books() -> tuple[books]:
    """Returns a tuple of all wrapped books in the database"""
    return add_wrapper_to_iter(exec_get_all("SELECT * FROM books;"), books)

def get_all_non_fiction() -> tuple[books]:
    """
    Get all non-fiction books in the database

    Returns a tuple of all books in the non-fiction genre
    """

    return add_wrapper_to_iter(exec_get_all("SELECT * FROM books WHERE books.genre = \'Non-Fiction\';"), books)

def get_all_fiction() -> tuple[books]:
    """
    Get all fiction books in the database

    Returns a tuple of all books in the fiction genre
    """

    return add_wrapper_to_iter(exec_get_all("SELECT * FROM books WHERE books.genre = \'Fiction\';"), books)

def make_username(member: members, uname: str = ''):
    """Sets a username for the given member.<br>If uname parameter is empty it will set to a default username"""
    id = member.map["members_id"]
    if uname == '':
        uname = "\'" + member.map["first_name"] + "_" + member.map["last_name"] + str(id) + "\'"
    exec_commit("UPDATE members SET username={0!s} WHERE members.members_id = {1!s};".format(uname, id))

def get_all_usernames(include_inactive: bool = False) -> tuple[str]:
    """returns all usernames in the database alphabetically"""
    tup_members = get_all_members(include_inactive)
    li = list()
    for member in tup_members:
        li.append(member.map["username"])
    li.sort()
    return tuple(li)

def build_default_usernames():
    """Makes default usernames (firstname+lastname+members_id) for all rows where username is \' \'"""
    allmembers = get_all_members()
    for member in allmembers:
        if member.map["username"] == '':
            make_username(member)

def get_reserved(books_id: int) -> int:
    """Gets who has a book reserved, if anyone. Returns an int"""
    book = book_lookup(books_id)
    if book != None:
        if book.map["reserved"] == 0:
            inv_tup = add_wrapper_to_iter(exec_get_all("SELECT * FROM inventory WHERE inventory.lent_to != 0 AND inventory.history_id = 0"), inventory)
            for inv in inv_tup:
                if inv.map["books_id"] == books_id:
                    return inv.map["lent_to"]
        else:
            return book.map["reserved"]
    else:
        return 0

def get_sum(table: str, col: str, args: str = "") -> int:
    """
    Gets count of some column in a table

    table: a table's name |
    column: a column within table |
    args: what would typically follow a Select-From statement to narrow down results. Defaults to empty

    returns an int    
    """

    return exec_get_one("SELECT SUM({0!s}) FROM {1!s} {2!s};".format(col, table, args))[0]


def get_max(table: str, col: str, args: str = "") -> int:
    """
    Gets max of some column in a table

    table: a table's name |
    column: a column within table |
    args: what would typically follow a Select-From statement to narrow down results. Defaults to empty

    returns an int    
    """

    return exec_get_one("SELECT MAX({0!s}) FROM {1!s} {2!s};".format(col, table, args))[0]

def get_min(table: str, col: str, args: str = "") -> int:
    """
    Gets min of some column in a table

    table: a table's name |
    column: a column within table |
    args: what would typically follow a Select-From statement to narrow down results. Defaults to empty

    returns an int    
    """

    return exec_get_one("SELECT MIN({0!s}) FROM {1!s} {2!s};".format(col, table, args))[0]

def get_count(table: str, col: str, args: str = "") -> int:
    """
    Gets a count of some column in a table. Typically the same as the highest primary key in a table

    table: a table's name |
    column: a column within table |
    args: what would typically follow a Select-From statement to narrow down results. Defaults to empty

    returns an int    
    """

    return exec_get_one("SELECT COUNT({0!s}) FROM {1!s} {2!s};".format(col, table, args))[0]

def get_all_overdue(date: datetime.date = datetime.date.today()) -> str:
    """
    Returns a string of all overdue books
    
    date: to adjust when the overdue date is
    """
    hist_tup = add_wrapper_to_iter(exec_get_all("SELECT * FROM history WHERE history.date_due < date(%s) AND history.date_returned IS NOT NULL ORDER BY members_id", (str(date),)), history)
    string = ""
    last_id = 0
    for hist in hist_tup:
        if string != "":
            string += "\n"
        m_id = hist.map["members_id"]
        if m_id != last_id:
            name = exec_get_one("SELECT first_name, last_name FROM members WHERE members.members_id = %s", (str(m_id),))
            string += name[0] + ' ' + name[1] + ":\n"
        string += "\t(" + str(hist.map["inventory_id"]) + ", " + str(hist.map["books_id"]) + ", " + str(hist.map["date_due"]) + ")"
        last_id = m_id
    return string

def create_history(info: tuple, date_lent: datetime.date = datetime.date.today(), date_due: datetime.date = datetime.date.today() + datetime.timedelta(days=14), date_returned: datetime.date = None) -> int:
    """
    Adds a row to the history table
    
    Format info as (inventory_id, books_id, members_id) then fill in other parameters as desired
    """
    inventory_id = info[0]
    books_id = info[1]
    members_id = info[2]

    hist_id = exec_insert_returning("INSERT INTO history(books_id, members_id, inventory_id, date_lent, date_due) VALUES %s RETURNING history_id;", ((str(books_id), str(members_id), str(inventory_id), str(date_lent), str(date_due)),) )
    if date_returned != None:
        add_returned_date(history_lookup(hist_id), date_returned)

    return hist_id

def add_returned_date(history: history, date_returned: datetime.date = datetime.date.today()):
    """
    Adds a returned date and calculates the late fee associated with it. Puts both in the table
    
    history: an inventory<br>
    date_returned: the date the book was returned
    """

    if history.map["date_returned"] != None:
        return 0
    else:
        fee = calculate_overdue_fee(history, date_returned)
        ret = 0
        if fee != 0:
            ret = fee[0]
        exec_commit("UPDATE history SET date_returned=%s, late_fee=%s WHERE history_id = %s", (str(date_returned), str(ret), str(history.map["history_id"])))
        return fee

def create_new_member(first_name: str, last_name: str, email: str, phonenumber: str, members_id: int = None, username: str = "", active: bool = True) -> int:
    """
    Creates a new member. Requires a dict of information containing at least a first name, last name, an email, and a phone number
    in that order

    Full structure is: (optional) members_id: int , (optional) username: str , first_name: str, last_name: str, email: str, phonenumber: str, (optional) active: boolean 

    returns a status code: 0 is success, 1 is fail
    """

    member = exec_get_one("SELECT * FROM members WHERE members.phonenumber = %s", (phonenumber,))
    if member == None:
        info = list()
        build_username = False
        string = ""
        if members_id != None:
            info.append(members_id)
            string += "members_id, "

        if username != "":
            info.append(username)
            string += "username, "
        else:
            build_username = True

        info.append(first_name)
        info.append(last_name)
        info.append(email)
        info.append(phonenumber)
        string += "first_name, last_name, email, phonenumber"
        if not active:
            info.append(active)
            string += ", active"

        info_tup = tuple(info)
        str_info = ""
        for item in info_tup:
            if str_info != "":
                str_info += ", "
            str_info += str(item)
        exec_commit("INSERT INTO members({0!s}) VALUES {1!s};".format(string, info_tup))
        if build_username:
            make_username(member_lookup_email(email))
        return 0
    else:
        return 1

def flip_member_id(member_id: int):
    """Flips if a member is active or not based on their member_id"""
    if get_checked_out(member_id) == '':
        member = member_lookup(member_id)
        choice = ""
        if member.map["active"]:
            choice = "False"
        else:
            choice = "True"
        exec_commit("UPDATE members SET active=%s WHERE members.members_id = %s;", (choice, str(member_id)))

def flip_member(member: members):
    """overload to take a members wrapper"""
    flip_member_id(member.map["members_id"])

def parse_csv(csv_filepath):
    """Reads and enters a CSV file into the database"""
    with open(csv_filepath, newline='') as csvfile:
        csvfile.readline()
        reader = csv.reader(csvfile)
        for line in reader:
            line[5]= int(line[5])
            create_book(line)

def create_book(info: tuple[str], library: str = ""):
    """
    Creates a book based off the information in the tuple<br>
    
    info is ordered as in the csv, ie Title, Author, Summary, Genre, Sub-Genre, and copies
    """

    book_tup = exec_get_all("SELECT * FROM books WHERE books.title = %s AND books.author = %s;", (info[0], info[1]))
    book_id = None
    if len(book_tup) == 0:
        li = list()
        for item in info:
            item = str(item).replace("'", "")
            item = item.replace("\"", "\'")
            if item.isdigit():
                li.append(int(item))
            else:
                li.append(item)
        li = tuple(li)
        exec_commit("INSERT INTO books(title, author, summary, genre, subgenre, in_stock) VALUES {0!s};".format(str(li)))
        book_id = exec_get_one("SELECT books_id FROM books WHERE books.title = %s AND books.author = %s;", (li[0], li[1]))[0]
    else:
        book_id = book_tup[0][0]
        if exec_get_one("SELECT summary FROM books WHERE books.summary = 'im a text, short and stout' and books.books_id = %s;", (book_id,)) == ('im a text, short and stout',):
            exec_commit("UPDATE books SET summary=%s WHERE books.books_id = %s;", (info[2], book_id))
        if exec_get_one("SELECT subgenre FROM books WHERE books.subgenre IS NULL AND books.books_id = %s;", (book_id,)) == ('',):
            exec_commit("UPDATE books SET subgenre=%s WHERE books.books_id = %s;", (info[4], book_id))
        originally = exec_get_one("SELECT in_stock FROM books WHERE books.books_id = %s", (book_id,))[0]
        exec_commit("UPDATE books SET in_stock=%s WHERE books.books_id = %s;", (info[5] + originally, book_id))
    for i in range(info[5]):
        if library == "":
            exec_commit("INSERT INTO inventory(books_id) VALUES (%s);", (str(book_id),))
        else:
            exec_commit("INSERT INTO inventory(books_id, library) VALUES (%s, %s);", (str(book_id), library))

def adjust_lent_date(hist: history, date_delta: datetime.timedelta = datetime.timedelta(days=0)):
    """Adds the timedelta to the lent date of a book"""
    date_lent = hist.map["date_lent"]
    exec_commit("UPDATE history SET date_lent=%s WHERE history.history_id = %s", (str(date_lent + date_delta), hist.map["history_id"], ))
    
def adjust_due_date(hist: history, date_delta: datetime.timedelta = datetime.timedelta(days=0)):
    """Adds the timedelta to the due date of a book"""
    exec_commit("UPDATE history SET date_due=%s WHERE history.history_id = %s", (hist.map["date_due"] + date_delta, hist.map["history_id"]))

def transfer_book(inv: inventory, library: str) -> int:
    """
    Transfers the books from one library to another within the system
    
    Valid library entires: "Penfield", "Fairport", "Henrietta", "Pittsford"
    
    Returns a status code: 0 for pass, 1 for fail
    """

    if is_valid_library(library):
        exec_commit("UPDATE inventory SET library=%s WHERE inventory.inventory_id = %s", (library, str(inv.map["inventory_id"])))
        return 0
    return 1

def randomize_libs():
    """Changes the location of all the not checked out books so that they are spread out evenly"""
    import random as ra
    di = {0: "Penfield", 1: "Fairport", 2: "Henrietta", 3: "Pittsford"}
    for inv in get_all_not_checked_out():
        rand = ra.randrange(4)
        transfer_book(inv, di[rand])

def calculate_days_late(turned_in: datetime.date, date_due: datetime.date) -> int:
    """
    Calculates how many days between turned_in and date_due

    Returns an int
    """

    return (turned_in - date_due).days

def calculate_overdue_fee(hist: history, date: datetime.date = datetime.date.today()) -> tuple:
    """
    Calculate the overdue fees for an inventoried book
    
    hist: history of the book's date with fee to be calculated<br>
    date: **TESTING ONLY** a function to adjust the date for unit testing

    returns (days_late, fee) | Nonw
    """

    date_due = hist.map["date_due"]
    if date < date_due:
        return 0
    days_late = calculate_days_late(date, date_due)
    fee = min(days_late, 7) * 0.25
    if days_late > 7:
        fee += (days_late - 7) * 2
    return (days_late, fee)

def _build_whitespace(length: int) -> str:
    """Helper function to make whitespace"""
    string = ""
    for i in range(length):
        string += " "
    return string

def create_array(headers : tuple = ("book", "name", "checkout_date", "returned_date", "late_fees"), args: tuple = ("title || ' by ' || books.author", "members.first_name || ' ' || members.last_name", "history.date_lent", "history.date_returned", "history.late_fee")):
    """
    Creates a printable array that takes information from the history table and joins them with all the other tables

    cols: a dict. Keys are the name to be put on the printable table. Values are the argument for the array_agg function

    returns a string
    """

    num_cols = len(headers)
    value = list() # list of lists

    # get all the values
    for arg in args:
        arr = exec_get_one("""SELECT array_agg({0!s} ORDER BY history.history_id) FROM history
	                            INNER JOIN books ON books.books_id = history.books_id
                                INNER JOIN members ON members.members_id = history.members_id
                                INNER JOIN inventory ON inventory.inventory_id = history.inventory_id""".format(arg))
        value.append(list(arr[0]))

    # filter everything to be str
    for i in range(len(value)):
        for j in range(len(value[i])):
            item = value[i][j]
            if type(item).__name__ != 'str':
                if item == None:
                    value[i][j] = "None"
                else:
                    value[i][j] = str(item)

    # get the maximum length of each column
    lengths = [0,0,0,0,0]
    longest = 0
    i = 0
    for item in headers:
        length = len(item)
        if length > longest:
            longest = length
        lengths[i] = longest
        i += 1
    for i in range(len(value)):
        longest = lengths[i]
        for j in range(len(value[i])):
            length = len(value[i][j])
            if length > longest:
                longest = length
        if lengths[i] < longest:
            lengths[i] = longest

    # build table
    tab_of_str = list()
    string = ""
    lower = ""
    for i in range(num_cols):
        # adds the column seperator
        if string != "":
            string += "|"
            lower += "+"
        # subtract half of the length by half of the header to find where to put it
        to_add = ""
        dist = (lengths[i] / 2) - (len(headers[i]) / 2)
        if dist > 0:
            substr = _build_whitespace(round(dist))
            to_add = " " + substr + headers[i] + substr + " "
        else:
            to_add = " " + headers[i] + " "
        string += to_add
        # build the lower seperator 
        for j in to_add:
            lower += "-"
             
    tab_of_str.append(string)
    tab_of_str.append(lower)

    # add the rest
    for j in range(len(value[0])):
        string = " "
        for i in range(len(value)):
            if string != " ":
                string += " | "
            item = value[i][j]
            diff = lengths[i] - len(item)
            space = _build_whitespace(diff)
            if len(value) - 1 == i:
                string += space + item
            else:
                string += item + space
        tab_of_str.append(string)
        

    # compile all the strings
    string = ""
    for row in tab_of_str:
        if string != "":
            string += '\n'
        string += row

    return string
