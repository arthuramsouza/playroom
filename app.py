from flask import Flask, render_template

app = Flask(__name__)


class Game:
    def __init__(self, name, genre, platform):
        self.name = name
        self.genre = genre
        self.platform = platform


@app.route('/')
def list():
    game1 = Game('Halo 2', 'Sci-fi', 'Xbox')
    game2 = Game('Red Dead Redemption', 'Action', 'Xbox 360')
    return render_template('list.html', title='Playroom', games=[game1, game2])


@app.route('/new')
def hello_world():
    return render_template('new.html', title='New game')


if __name__ == '__main__':
    app.run()
