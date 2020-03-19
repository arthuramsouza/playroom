from flask import Flask, redirect, render_template, request

app = Flask(__name__)


class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform


game_list = [Game('Halo 2', 'Sci-fi', 'Xbox'), Game('Red Dead Redemption', 'Action', 'Xbox 360')]


@app.route('/')
def index():
    return render_template('list.html', title='Playroom', games=game_list)


@app.route('/new')
def new():
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
