INSERT INTO history(books_id, members_id, inventory_id, date_lent, date_due) VALUES
(1, 4, 1, date(now()), date(now() + interval '2 weeks')),
(2, 5, 11, date(now()), date(now() + interval '2 weeks')),
(3, 6, 18, date(now()), date(now() + interval '2 weeks')),
(4, 6, 22, date(now()), date(now() + interval '2 weeks'));