from itertools import groupby
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5


def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

bootstrap = Bootstrap5(app)


@app.route('/')
@app.route('/index')
def index():
    conn = get_db_connection()
    todos = conn.execute(
        'SELECT i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;'
    ).fetchall()

    lists = {}

    for key, group in groupby(todos, key=lambda row: row['title']):
        lists[key] = list(group)

    conn.close()
    return render_template('index.html', lists=lists)
