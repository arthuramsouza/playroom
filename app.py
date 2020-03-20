import os
from flask import Flask, flash, redirect, render_template, request, session

app = Flask(__name__)
app.secret_key = os.urandom(16)


class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform


game_list = [Game('Halo 2', 'Sci-fi', 'Xbox'), Game('Red Dead Redemption', 'Action', 'Xbox 360')]


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
    if request.form['password'] == 'admin':
        session['logged_user'] = request.form['username']
        flash('{}, you are now logged in!'.format(request.form['username']), 'success')
        return redirect('/{}'.format(next_page))
    else:
        flash('Something went wrong. Please, check your credentials and try again.', 'danger')
        return redirect('/login?next_page=new')


@app.route('/logout')
def logout():
    session['logged_user'] = None
    flash('You are now logged out', 'success')
    return redirect('/')


@app.route('/new')
def new():
    if 'logged_user' not in session or session['logged_user'] is None:
        flash('You must login before creating a new game.', 'danger')
        return redirect('/login?next_page=new')
    return render_template('new.html', title='New game')


@app.route('/create', methods=['POST'])
def create():
    name = request.form['name']
    genre = request.form['genre']
    platform = request.form['platform']
    game_list.append(Game(name, genre, platform))
    return redirect('/')


if __name__ == '__main__':
    app.run()
