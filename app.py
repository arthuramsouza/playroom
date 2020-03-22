import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_mysqldb import MySQL

from dao import GameDAO
from models import Game, User

app = Flask(__name__)
app.secret_key = os.urandom(16)
app.config.from_object('config')
db = MySQL(app)

game_dao = GameDAO(db)

user1 = User('arthur', 'Arthur Menezes', '1234')
user2 = User('admin', 'Admin', 'admin')
user3 = User('masterchief', 'John-117', 'cortana')

users = {user1.username: user1,
         user2.username: user2,
         user3.username: user3}

game_list = [Game('Halo 2', 'Sci-fi', 'Xbox'),
             Game('Red Dead Redemption', 'Action', 'Xbox 360')]


@app.route('/')
def index():
    return render_template('list.html', title='Playroom', games=game_list)


@app.route('/login')
def login():
    next_page = request.args.get('next_page')
    return render_template('login.html', title='Login', next_page=next_page)


@app.route('/authenticate', methods=['POST'])
def authenticate():
    next_page = request.form['next_page']
    if request.form['username'] in users:
        user = users[request.form['username']]
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
    game_dao.save(Game(name, genre, platform))
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
