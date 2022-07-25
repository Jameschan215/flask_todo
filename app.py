from itertools import groupby
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired


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


@app.route('/create', methods=['GET', 'POST'])
def create():
    conn = get_db_connection()
    lists = conn.execute('SELECT title FROM lists;').fetchall()
    form = TodoForm()
    conn.close()

    return render_template('create.html', form=form, lists=lists)


class TodoForm(FlaskForm):
    title = SelectField(
        label='Title', validators=[DataRequired()],
        choices=[(1, 'Work'), (2, 'Home'), (3, 'Study')],
        default=1, coerce=int
    )
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')
