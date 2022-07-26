from itertools import groupby
from app import get_db_connection

conn = get_db_connection()
todos = conn.execute('SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l \
                        ON i.list_id = l.id ORDER BY l.title;').fetchall()

lists = {}

for k, g in groupby(todos, key=lambda t: t['title']):
    # Create an empty list for items
    items = []

    # Go through each to-do item row in the groupby() grouper object
    for item in g:
        assignees = conn.execute(
            'SELECT a.id, a.name FROM assignees a JOIN item_assignees i_a '
            'ON a.id = i_a.assignee_id WHERE i_a.item_id = ?',
            (item['id'],)
        ).fetchall()

        # Convert the item row into a dictionary to add assignees
        item = dict(item)
        item['assignees'] = assignees
        items.append(item)

    # lists[k] = list(g)
    lists[k] = items

for list_, items in lists.items():
    print(list_)
    for item in items:
        assignee_names = ', '.join([a['name'] for a in item.get('assignees')])
        print('    ', item['content'], '| id:', item['id'], '| done:', item['done'], '| assignees:', assignee_names)
