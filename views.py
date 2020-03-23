import os
import time

from flask import render_template, request, session, flash, redirect, url_for, send_from_directory

from app import app, db
from dao import GameDAO, UserDAO
from helpers import get_image_filename, delete_image
from models import Game

game_dao = GameDAO(db)
user_dao = UserDAO(db)


@app.route('/')
def index():
    return render_template('list.html', title='Playroom', games=game_dao.list())


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    next_page = request.form['next_page']
    user = user_dao.search_by_id(request.form['username'])
    if user:
        if request.form['password'] == user.password:
            session['logged_user'] = user.username
            flash('{}, you are now logged in!'.format(user.name), 'success')
            return redirect(next_page)
    else:
        flash('Something went wrong. Please, check your credentials and try again.', 'danger')
        return redirect(url_for('login', next_page=url_for('new')))


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        flash('You must login before creating a new game.', 'danger')
        return redirect(url_for('login', next_page=url_for('new')))
    return render_template('new.html', title='New game')


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    genre = request.form['genre']
    platform = request.form['platform']
    game = game_dao.save(Game(name, genre, platform))
    delete_image(game.id)
    artwork = request.files['artwork']
    if artwork.filename != '':
        artwork.save(os.path.join(app.config['UPLOAD_PATH'], 'artwork_{}_{}.jpg'.format(game.id, time.time())))
    return redirect(url_for('index'))


@app.route('/edit/<int:id>')
def edit(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        flash('You must login before editing a game.', 'danger')
        return redirect(url_for('login', next_page=url_for('edit', id=id)))
    game = game_dao.search_by_id(id)
    return render_template('edit.html', title='Edit game', game=game, artwork=get_image_filename(id))


@app.route('/update', methods=['POST'])
def update():
    id = request.form['id']
    name = request.form['name']
    genre = request.form['genre']
    platform = request.form['platform']
    game = game_dao.save(Game(name, genre, platform, id))
    delete_image(game.id)
    artwork = request.files['artwork']
    if artwork.filename != '':
        artwork.save(os.path.join(app.config['UPLOAD_PATH'], 'artwork_{}_{}.jpg'.format(game.id, time.time())))
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def delete(id):
    if 'logged_user' not in session or session['logged_user'] is None:
        flash('You must login before deleting a game.', 'danger')
        return redirect(url_for('login', next_page=url_for('delete', id=id)))
    game_dao.delete(id)
    flash('The game has been deleted.', 'success')
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def image(filename):
    return send_from_directory('uploads', filename)
