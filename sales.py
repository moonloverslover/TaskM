import sqlite3 as lite
import sys

sales = (

    ('John', 22000),
    ('Lily', 25000)


)


con = lite.connect('sales.db')

with con:

	cur = con.cursor()

	cur.execute("DROP TABLE IF EXISTS REPS")
	cur.execute("CREATE TABLE reps(rep_name TEXT, amount INT)")
	cur.executemany("INSERT INTO reps VALUES(?,?)",sales)











