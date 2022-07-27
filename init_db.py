import sqlite3

# Initialize the database

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

# Write fake data in

# Write title in lists
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Work',))
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Home',))
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Study',))

# Write content and id of list in items
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (1, 'Morning meeting'))

cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (2, 'Buy fruit'))
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (2, 'Cook dinner'))

cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (3, 'Learn Flask'))
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (3, 'Learn SQLite'))

# commit to database and close the connection
connection.commit()
connection.close()
