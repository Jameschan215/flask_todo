import sqlite3

# Initialize the database

connection = sqlite3.connect('database.db')
with open('schema.sql') as f:
    connection.executescript(f.read())
cur = connection.cursor()

# Write fake data in

# Write title in lists
cur.execute('INSERT INTO lists (title) VALUES (?)', ('New List',))
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Work',))
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Home',))
cur.execute('INSERT INTO lists (title) VALUES (?)', ('Study',))

# Write content and id of list in items
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (2, 'Morning meeting'))

cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (3, 'Buy fruit'))
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (3, 'Cook dinner'))

cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (4, 'Learn Flask'))
cur.execute('INSERT INTO items (list_id, content) VALUES (?, ?)', (4, 'Learn SQLite'))

cur.execute('INSERT INTO assignees (name) VALUES (?)', ('Sammy',))
cur.execute('INSERT INTO assignees (name) VALUES (?)', ('Jo',))
cur.execute('INSERT INTO assignees (name) VALUES (?)', ('Charlie',))
cur.execute('INSERT INTO assignees (name) VALUES (?)', ('Ashley',))

# Assign 'Morning meeting' to 'Sammy'
cur.execute('INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)', (1, 1))

# Assign 'Morning meeting' to 'Jo'
cur.execute('INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)', (1, 2))

# Assign 'Morning meeting' to 'Ashley'
cur.execute('INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)', (1, 4))

# Assign 'Buy fruit' to 'Sammy'
cur.execute('INSERT INTO item_assignees (item_id, assignee_id) VALUES (?, ?)', (2, 1))

# commit to database and close the connection
connection.commit()
connection.close()
