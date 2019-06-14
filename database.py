import sqlite3

conn = sqlite3.connect('database.db')

cur = conn.cursor()

print ("Opened database successfully")

# 23
# NOTE:
# In SQLite, INTEGER PRIMARY KEY column is auto-incremented. There is also an AUTOINCREMENT keyword.
# When used in INTEGER PRIMARY KEY AUTOINCREMENT, a slightly different algorithm for Id creation is used.
conn.execute('CREATE TABLE if not exists users (id Integer Primary Key, username TEXT, password TEXT)')
print ("Table created successfully")

conn.execute('CREATE TABLE if not exists items (id Integer Primary Key, name TEXT, price TEXT)')
print ("Table created successfully")

user = [(1,"jose","asdf"),(2,"myk","qwer"),(3,"kirti","zxcv")]

cur.executemany('INSERT INTO users VALUES (?,?,?)',user)


conn.commit()

conn.close()
