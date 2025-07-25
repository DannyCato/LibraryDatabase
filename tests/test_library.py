import unittest
import datetime
from src import TABLES
from src.library import *
from tests.seed import *

"""
For testing functions in library.py
"""
class TestLibrary(unittest.TestCase):
    """Know of the dangers of string concatenation but while there is no user input I will not worry about it"""

    def test_a_rebuild_tables(self):
        """Build the tables"""
        rebuildTables()
        for table in TABLES:
            result = exec_get_all('SELECT * FROM ' + table)
            self.assertEqual([], result, table + " has values and was not reset")

    def test_b_rebuild_tables_is_idempotent(self):
        """Drop and rebuild the tables twice"""
        rebuildTables()
        rebuildTables()
        for table in TABLES:
            result = exec_get_all('SELECT * FROM '+ table)
            self.assertEqual([], result, "no rows in " + table)

    def test_c_fill_tables(self):
        seed_book1()
        seed_member1()
        seed_member2()
        seed_inventory1()
        seed_history1()
        build_default_usernames()

    def test_cb_tables_not_empty(self):
        self.assertTrue(TABLES.__contains__("books"), "TABLES is empty and subsequent tests will throw errors")

    def test_cc_inventory_columns(self):
        """compares the max inventory_id to the sum of in_stock books to tell if all the books got created"""
        self.assertEqual(get_max("inventory", "inventory_id"), get_sum("books", "in_stock"),"incorrect number of rows were found in inventory")

    def test_cd_read_csv(self):
        start = get_max("books", "books_id")
        parse_csv(DIR_PATH + "Library.csv")
        end = get_max("books", "books_id") # not 19 because of an overlap with other seed data. good way to force collision code though!
        self.assertEqual(end - start, 18, "An incorrect number of books were added")
        self.assertEqual(get_sum("books", "in_stock"), 139, "books were not added to inventory table")

    def test_ce_libraries(self):
        for lib in {"Penfield", "Fairport", "Henrietta", "Pittsford"}:
            self.assertTrue(is_valid_library(lib), "Something is wrong")

    def test_d_lookup_id(self):
        book = book_lookup(1)
        self.assertEqual(str((1, 'Fahrenheit 451', 'Ray Bradbury', datetime.date(1953, 10, 19), '978-1451673319', 'Fiction', 'Science Fiction', 'im a text, short and stout', 10, 1, 0)), str(book.tup), "The books are not the same")

    def test_e_lookup_title(self):
        book = book_lookup_t("The Scarlet Letter")[0]
        self.assertEqual((3, 'The Scarlet Letter', 'Nathaniel Hawthorne', datetime.date(1850, 3, 16), '979-8800923414', 'Fiction', 'Literature', 'im a text, short and stout', 4, 1, 0), book.tup, "The books are not the same")

    def test_f_lookup_isbn(self):
        book = book_lookup_i("978-0679745587")
        self.assertEqual((5, 'In Cold Blood', 'Truman Capote', datetime.date(1994, 2, 1), '978-0679745587', 'Non-Fiction', 'Crime', 'In school we only learn to recognize the words and to spell', 7, 0, 0), book.tup, "The books are not the same")

    def test_g_lookup_member(self):
        member = member_lookup(3)
        self.assertEqual((3, 'SchoolLunches','Michelle', 'Obama', 'mo@whitehouse.gov', '1234567890', 0, True), member.tup, "Two different people were picked")

    def test_ga_lookup_inv_mem(self):
        member = member_lookup(4)
        inv_m = inv_lookup_m(member)
        today = datetime.date.today()
        weeks2 = datetime.timedelta(weeks=2)
        self.assertEqual(inv_m[0].tup, (1, 1, 4, 1, "Henrietta"), "Member does not have this book checked out")

    def test_gb_lookup_inv_(self):
        book = book_lookup(1)
        inv_b = inv_lookup_b(book)
        self.assertEqual(inv_b[0].tup, (1, 1, 4, 1, "Henrietta"), "The implied book was not found")      

    def test_gd_lookup_inv_id(self):
        inv_i = inv_lookup(id = 1)
        self.assertEqual(inv_i.tup, (1, 1, 4, 1, "Henrietta"), "The implied book was not found")      

    def test_ge_lookup_member_phone(self):
        member = member_lookup_phone("1111111111")
        self.assertEqual((5, 'Mary_Shelley5','Mary', 'Shelley', 'Mary@shelley.com', '1111111111', 0, True), member.tup, "Two different people were picked")

    def test_gf_lookup_member_email(self):
        member = member_lookup_email("mo@whitehouse.gov")
        self.assertEqual((3, 'SchoolLunches','Michelle', 'Obama', 'mo@whitehouse.gov', '1234567890', 0, True), member.tup, "Two different people were picked")

    def test_gg_is_active(self):
        self.assertTrue(is_active(3), "Member is not being fetched")

    def test_gh_flip_member(self):
        flip_member_id(3)
        self.assertFalse(is_active(3), "Member is not being gotten")
        flip_member_id(3)

    def test_h_check_out_book(self):
        member = member_lookup(2) # Barack
        book = book_lookup(1)
        book_checkout(member, book, "Henrietta")
        self.assertEqual(get_checked_out(2)[0].map["title"], 'Fahrenheit 451', "A book was not checked out")

    def test_i_Garfunkel_checked_out(self):
        self.assertEqual(get_checked_out(7), '', "Art Garfunkel has a book when they should not or it is null")

    def test_ia_Gleason_checked_out(self):
        self.assertEqual(get_checked_out(6, asString= True), "6: (The Diary of a Young Girl, The Scarlet Letter)")

    def test_j_get_all_fiction(self):
        """Tests the length of the list of all fiction books to gauge how many were registered"""
        self.assertEqual(len(get_all_fiction()), 15, "An incorrect number of books are listed")

    def test_k_get_all_non_fiction(self):
        """Tests the length of the list of all non-fiction books to gauge how many were registered"""
        self.assertEqual(len(get_all_non_fiction()), 9, "An incorrect number of books are listed")

    #def test_ka_get_all

    def test_l_all_checked_out(self):
        """Checking if function matches test data set"""
        dic = get_all_checked_out()
        check = False
        if dic.keys().__contains__(2) and dic[2] == 1:
            if dic.keys().__contains__(4) and dic[4] == 1:
                if dic.keys().__contains__(5) and dic[5] == 2:
                    if dic.keys().__contains__(6) and dic[6] == (3, 4):
                        check = True
        self.assertTrue(check, "returned dictonary is incorrect or data has been altered")

    def test_m_all_checked_out_str(self):
        """Checking if function matches test data set"""
        tup = get_all_checked_out(returnAsString= True)
        self.assertEqual(tup, "{{{ObamaOut: (Fahrenheit 451)}, {Ada_Lovelace4: (Fahrenheit 451)}, {Mary_Shelley5: (1984)}, {Jackie_Gleason6: (The Scarlet Letter, The Diary of a Young Girl)}}}")

    def test_n_checkout_single_book(self):
        book = book_lookup_t("A Brief History of Time")[0] # picked because it has one copy
        member = member_lookup(1)
        status = book_checkout(member, book, "Henrietta")
        self.assertEqual(status, 0, "Something else happened to the book")

    def test_na_reserved_Jackie(self):
        """Jackie Gleason reserves a book"""
        book = book_lookup_t("A Brief History of Time")[0]
        member = member_lookup(6)
        status = book_checkout(member, book, "Henrietta")
        self.assertEqual(status, 2, "Book was not reserved")
        id = get_reserved(book.map["books_id"])
        self.assertEqual(member.map["members_id"], id, "!!")

    def test_nb_reserved_fail(self):
        book = book_lookup_t("A Brief History of Time")[0]
        member = member_lookup(2)
        status = book_checkout(member, book, "Henrietta")
        self.assertEqual(status, 1)

    def test_nc_checkout_overdue(self):
        member = member_lookup(6)
        inv = inv_lookup_m(member)[0]
        book = book_lookup(inv.map["books_id"])
        hist = history_lookup_member_book(member, book)
        h_id = hist.map["history_id"]
        delta = datetime.timedelta(weeks=-3.0)
        adjust_lent_date(hist, delta)
        adjust_due_date(hist, delta)
        hist = history_lookup(h_id)
        self.assertTrue(hist.map["date_due"] < datetime.date.today(), "Should be one week from today")
        status = book_checkout(member, book_lookup(hist.map["books_id"]), "Henrietta")
        self.assertEqual(status, -1, "Status -1 because of having an overdue book")
        delta = datetime.timedelta(weeks=3.0)
        adjust_lent_date(hist, delta)
        adjust_due_date(hist, delta)

    def test_nd_return(self):
        member = member_lookup(1)
        book = book_lookup_t("A Brief History of Time")[0]  
        status = book_returned(member, book.map["books_id"])
        self.assertEqual(status, None, "Book was unsuccessfully returned")

    def test_ne_checkout_reserved(self):
        book = book_lookup_t("A Brief History of Time")[0]
        member = member_lookup(get_reserved(book.map["books_id"]))
        status = book_checkout_reserved(member)
        self.assertEqual(status, 0, "Failed to check out book")

    def test_o_create_new_member_Marlowe(self):
        """Christopher Marlow Creation"""
        status = create_new_member("Christopher", "Marlowe", "cm@gmail.com", "9874563210")
        self.assertEqual(status, 0, "Failed to create member")

    def test_oa_create_new_member_Bacon(self):
        """Francis Bacon Creation"""
        status = create_new_member("Francis", "Bacon", "fb@gmail.com", "1236547890")
        self.assertEqual(status, 0, "Failed to create member")

    def test_p_Garfunkel_due_date(self):
        """Garfunkel Checks out Frankenstein for 3 days and returns it"""
        title = "Frankenstein"
        author = "Mary Shelly"
        summary = "a young scientist creates a sapient creature in an unorthodox scientific experiment"
        genre = "Fiction"
        subgenre = "Science Fiction"
        copies = 2
        create_book((title, author, summary, genre, subgenre, copies))
        book = book_lookup_t("Frankenstein")[0]
        self.assertTrue(book != None, "Frankenstien was not created")

        member = member_lookup(7)
        status = book_checkout(member, book, "Henrietta")
        self.assertEqual(status, 0)
        hist = history_lookup_member_book(member, book)
        adjust_lent_date(hist, datetime.timedelta(days= -3))
        self.assertEqual(hist_dates(hist.map["history_id"])["date_lent"], datetime.date.today() + datetime.timedelta(days= -3), "The date was not adjusted")
        
        status = book_returned(member, book.map["books_id"])
        self.assertEqual(status, None, "Book was not returned for some reason")

    def test_q_Shelly_Search_Disable(self):
        """Looks up \'The Last Man\', finds nothing, rage quits"""
        member = member_lookup(5)
        status = book_returned(member, 2)
        self.assertEqual(status, None, "Mary's book was returned")

        book = book_lookup_t("The Last Man")
        self.assertEqual(book, (), "A books was found??")
        
        flip_member(member)
        self.assertFalse(is_active(member.map["members_id"]), "Mary Shelly's account was not disabled")

    def test_qa_get_all_ever_checked_out(self):
        string = get_all_ever_checked_out()
        today = str(datetime.date.today())
        day3 = str(datetime.date.today() - datetime.timedelta(days=3))
        due = str(datetime.date.today() + datetime.timedelta(weeks=2))
        self.maxDiff = None
        self.assertEqual(string, 
"""{{
{inv_id: 2, Barack Obama: Checked out Fahrenheit 451 on """ + today + " due on " + due + """ not returned yet, in stock: 10}
{inv_id: 1, Ada Lovelace: Checked out Fahrenheit 451 on """ + today + " due on " + due + """ not returned yet, in stock: 10}
{inv_id: 18, Jackie Gleason: Checked out The Scarlet Letter on """ + today + " due on " + due + """ not returned yet, in stock: 4}
{inv_id: 11, Mary Shelley: Checked out 1984 on """ + today + " due on " + due + " and returned on " + today + """, in stock: 7}
{inv_id: 140, Art Garfunkel: Checked out Frankenstein on """ + day3 + " due on " + due + " and returned on " + today + """, in stock: 2}
{inv_id: 22, Jackie Gleason: Checked out The Diary of a Young Girl on """ + today + " due on " + due + """ not returned yet, in stock: 5}
{inv_id: 104, Mr. Rogers: Checked out A Brief History of Time on """ + today + " due on " + due + " and returned on " + today + """, in stock: 1}
{inv_id: 104, Jackie Gleason: Checked out A Brief History of Time on """ + today + " due on " + due + """ not returned yet, in stock: 1}
}}""", "Strings do not match")
        
    def test_r_randomize_libs(self):
        randomize_libs()
        di = {0: "Penfield", 1: "Fairport", 2: "Henrietta", 3: "Pittsford"}
        for i in range(4):
            self.assertTrue(get_count("inventory", "library", "WHERE inventory.library = \'%s\'" % di[i]) > 0, "The books did not get reset")

    def test_s_add_Winds_Of_Winter(self):
        title = "The Winds of Winter"
        author = "George R.R. Martin"
        summary = "kickflip off a balcony"
        genre = "Fiction"
        subgenre = "Literature"
        copies = 1
        create_book((title, author, summary, genre, subgenre, copies), "Fairport")
        book_lookup_t(title)[0]
        self.assertTrue(title != None, "Books was not created")

    def test_sb_checkouts_WoW(self):
        WoW = book_lookup_t("The Winds of Winter")[0]

        d1 = datetime.date(2024, 1, 2)
        Mary = member_lookup_email("Mary@shelley.com")
        flip_member(Mary) #reactivate Mary
        status = book_checkout(Mary, WoW, "Fairport", d1)
        self.assertEqual(status, 0, "Book was not checked out")
        status = book_returned(Mary, WoW.map["books_id"], d1 + datetime.timedelta(days=8))
        self.assertEqual(status, None, "Book was not returned")

        d2 = datetime.date(2024, 1, 13)
        Ada = member_lookup_email("ada@lovelace.com")
        status = book_checkout(Ada, WoW, "Fairport", d2)
        self.assertEqual(status, 0, "Book was not checked out")

        d2 = d2 + datetime.timedelta(days=15)
        book = book_lookup(12)
        status = book_checkout(Ada, book, "Fairport", d2)
        self.assertEqual(status, -1, "Checkout was not denied for having an overdue")

        status = book_returned(Ada, WoW.map["books_id"], d2 + datetime.timedelta(days=3))
        self.assertNotEqual(status, 0, "Book was not returned")

        Jackie = member_lookup_email("jg@gmail.com")
        d3 = datetime.date(2024, 3, 1)
        status = book_checkout(Jackie, WoW, "Fairport", d3)
        self.assertEqual(status, 0, "Book was not checked out")

        status = book_returned(Jackie, WoW.map["books_id"], d3 + datetime.timedelta(days=30))
        self.assertNotEqual(status, 0, "Book was not returned")

    def test_sba_overdue_books(self):
        res = get_all_overdue(datetime.date.today() + datetime.timedelta(days=15))
        date = str(datetime.date.today() + datetime.timedelta(weeks=2))
        self.assertEqual(res, "Mr. Rogers:\n\t(104, 15, "+date+")\nAda Lovelace:\n\t(142, 26, 2024-01-27)\nMary Shelley:\n\t(11, 2, "+date+")\n\t(142, 26, 2024-01-16)\nJackie Gleason:\n\t(142, 26, 2024-03-15)\nArt Garfunkel:\n\t(140, 25, "+date+")", "Are not equal")

    def test_sc_more_copies_WoW(self):
        title = "The Winds of Winter"
        author = "George R.R. Martin"
        summary = "kickflip off  a balcony"
        genre = "Fiction"
        subgenre = "Literature"
        copies = 3
        WoW = book_lookup_t(title)[0]
        create_book((title, author, summary, genre, subgenre, copies), "Fairport")
        self.assertEqual(get_count("inventory", "inventory_id", "WHERE inventory.books_id = %s" % WoW.map["books_id"]), 4)

    def test_sd_fake_copies_WoW(self):
        title = "The Wines of Winter"
        author = "WineExpress"
        summary = "lmao"
        genre = "Non-Fiction"
        subgenre = "Natural Science"
        copies = 2
        create_book((title, author, summary, genre, subgenre, copies), "Pittsford")
        create_book((title, author, summary, genre, subgenre, copies), "Henrietta")
        WoW = book_lookup_t(title)[0]
        self.assertEqual(WoW.map["in_stock"], 4, "Not all copies were added")

    def test_se_report_all(self):
        self.assertTrue(get_report_all() != "", "Nothing was added")

    def test_t_abcd(self):
        print("\n")
        print(create_array())

    def test_ta_abcde(self):
        print("\n")
        print(report_all_ever_checked_out())