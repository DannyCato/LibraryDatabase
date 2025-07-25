-- Made in PostgreSQL 14's query tool and saved here 

DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS members;
DROP TABLE IF EXISTS inventory;
DROP TABLE IF EXISTS history;
DROP TYPE IF EXISTS category;
DROP TYPE IF EXISTS subcategory;
DROP TYPE IF EXISTS libs;

CREATE TYPE category AS ENUM('Fiction', 'Non-Fiction');
CREATE TYPE subcategory as ENUM('Literature', 'Science Fiction', 'History', 
								  'Science', 'Crime', 'Natural Science', 
								  'Social Sciences');
CREATE TABLE books(
	books_id		SERIAL PRIMARY KEY,
	title			TEXT NOT NULL DEFAULT '',
	author 			TEXT NOT NULL DEFAULT '',
	published		DATE,						-- MM-DD-YYYY
	isbn			TEXT NOT NULL DEFAULT '',
	genre			category NOT NULL,
	subgenre		subcategory,
	summary			TEXT DEFAULT 'im a text, short and stout',
	in_stock		INTEGER NOT NULL,
	lended			INTEGER NOT NULL DEFAULT 0,
	reserved		INTEGER NOT NULL DEFAULT 0	-- MEMBER_ID unique to the book so the first one that's free gets claimed
);

-- INSERT INTO books(id, title, author, genre, isbn, published, in_stock, lended) VALUES
-- 	(1, 'Fahrenheit 451', 'Ray Bradbury', 'Fiction', '978-1451673319', '10-19-1953', 1, 0),
-- 	(2, '1984', 'George Orwell', 'Fiction', '978-0451524935', '06-08-1949', 2, 2),
-- 	(3, 'The Scarlet Letter', 'Nathaniel Hawthorne', 'Fiction', '979-8800923414', '03-16-1850', 1, 1);

CREATE TABLE members(
	members_id		SERIAL PRIMARY KEY,
	username		TEXT NOT NULL DEFAULT '',
	first_name 		TEXT NOT NULL,
	last_name 		TEXT NOT NULL,
	email			TEXT NOT NULL,
	phonenumber 	TEXT NOT NULL,
	reserved		INTEGER DEFAULT 0,			-- BOOKS_ID
	active			BOOLEAN DEFAULT TRUE
);

-- INSERT INTO members(id, first_name, last_name, email, phonenumber, checked_out) VALUES
-- 	(1, 'Mr.', 'Rogers', 'mr@gmail.com', '1234567890', ''),
-- 	(2, 'Barack', 'Obama', 'bo@whitehouse.gov', '1234567890', '2'),
-- 	(3, 'Michelle', 'Obama', 'mo@whitehouse.gov', '1234567890', '2-3');

CREATE TYPE libs AS ENUM('Penfield', 'Fairport', 'Henrietta', 'Pittsford');
CREATE TABLE inventory(
	inventory_id	SERIAL PRIMARY KEY,
	books_id		INTEGER NOT NULL,			-- BOOKS_ID
	lent_to			INTEGER NOT NULL DEFAULT 0,	-- Can be not lent		MEMBER_ID
	history_id		INTEGER NOT NULL DEFAULT 0,
	library			libs DEFAULT 'Henrietta'
);

CREATE TABLE history(
	history_id		SERIAL PRIMARY KEY,
	books_id		INTEGER NOT NULL,
	members_id		INTEGER NOT NULL,
	inventory_id	INTEGER NOT NULL,
	date_lent		DATE NOT NULL,
	date_due		DATE NOT NULL,
	date_returned	DATE DEFAULT NULL,
	late_fee		DECIMAL(5,2) NOT NULL DEFAULT 0
)