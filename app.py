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
    form.title.choices = [(i, item['title']) for (i, item) in enumerate(lists)]

    if form.validate_on_submit():
        content = form.content.data

        # 这里 form.title.data 获取的是choices列表中元组的第一项，即(0, 'Work')中的0,
        # 为了取出Work，要把choices转成字典，把data，也就是0，当作键值，才能实现。
        list_title = dict(form.title.choices).get(form.title.data)

        if not content:
            flash('Content is required!')

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);', (list_title,)).fetchone()['id']
        conn.execute('INSERT INTO items (list_id, content) VALUES (?, ?);', (list_id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index', title=list_title))

    conn.close()
    return render_template('create.html', form=form, lists=lists)


class TodoForm(FlaskForm):

    title = SelectField('Title', coerce=int)
    content = StringField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')


