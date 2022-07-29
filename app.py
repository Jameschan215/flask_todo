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
        'SELECT i.id, i.done, i.content, l.title FROM items i JOIN lists l ON i.list_id = l.id ORDER BY l.title;'
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
    form.title.choices = [(i + 1, item['title']) for (i, item) in enumerate(lists)]
    form.new_list_title.render_kw = {'placeholder': 'New Title...'}
    form.content.render_kw = {'placeholder': 'Do something...'}


    if form.validate_on_submit():
        content = form.content.data

        # 这里 form.title.data 获取的是choices列表中元组的第一项，即(0, 'Work')中的0,
        # 为了取出Work，要把choices转成字典，把data，也就是0，当作键值，才能实现。
        list_title = dict(form.title.choices).get(form.title.data)
        new_list = form.new_list_title.data

        if list_title == 'New List' and new_list:
            li = conn.execute('SELECT * FROM lists WHERE title = ?', (new_list,))
            if li:
                flash('Same title!')
                return redirect(url_for('create'))
            conn.execute('INSERT INTO lists (title) VALUES (?)', (new_list,))
            conn.commit()
            list_title = new_list

        if not content:
            flash('Content is required!')

        list_id = conn.execute('SELECT id FROM lists WHERE title = (?);', (list_title,)).fetchone()['id']
        conn.execute('INSERT INTO items (list_id, content) VALUES (?, ?);', (list_id, content))
        conn.commit()
        conn.close()
        return redirect(url_for('index', title=list_title))

    conn.close()
    return render_template('create.html', form=form, lists=lists)


@app.route('/<int:id>/do', methods=['POST'])
def do(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:id>/undo', methods=['POST'])
def undo(id):
    conn = get_db_connection()
    conn.execute('UPDATE items SET done = 0 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


@app.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    todo = conn.execute(
        'SELECT i.id, i.list_id, i.done, i.content, l.title \
        FROM items i JOIN lists l ON i.list_id = l.id WHERE i.id = ?',
        (id,)
    ).fetchone()

    lists = conn.execute('SELECT title FROM lists;').fetchall()
    form = TodoForm()

    # i starts from 0, lists starts from 1, so i plus 1
    form.title.choices = [(i + 1, item['title']) for (i, item) in enumerate(lists)]

    # 这一行会把原有的值带入content的form中，但是当你submit的时候，新值不会带回来，content.data依然是原来的值
    # form.content.data = todo['content']
    # 使用render_kw可以完美解决这个问题
    form.content.render_kw = {'value': todo['content']}

    # Set SelectField's data with value of list's index plus 1
    form.title.data = todo['list_id']
    form.new_list_title.render_kw = {'placeholder': 'New Title...'}

    # form.title.default = todo['list_id']
    # form.process()
    # If you use 'default', you have to use 'process()' to make it work, but process will break csrf.
    # So you can just change 'default' to 'data', that works well and will not break anything.

    if form.validate_on_submit():
        content = form.content.data
        list_title = dict(form.title.choices).get(form.title.data)

        if not content:
            flash('Content is required!')
            return redirect(url_for('edit', id=id))

        flash(f'Content is "{content}"!')

        list_id = conn.execute('SELECT id FROM lists WHERE title = ?', (list_title,)).fetchone()['id']

        conn.execute('UPDATE items SET content = ?, list_id = ? WHERE id = ?', (content, list_id, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('edit.html', form=form)


@app.route('/<int:id>/delete', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM items WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


class TodoForm(FlaskForm):
    title = SelectField('Title', coerce=int, validators=[DataRequired()])
    content = StringField('Content', validators=[DataRequired()])
    new_list_title = StringField('New List', validators=[DataRequired()])

    submit = SubmitField('Submit')



