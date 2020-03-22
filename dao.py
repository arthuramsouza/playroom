from models import Game, User

# Queries
SQL_INSERT_GAME = 'INSERT into game (name, genre, platform) values (%s, %s, %s)'
SQL_UPDATE_GAME = 'UPDATE game SET name=%s, genre=%s, platform=%s where id = %s'
SQL_DELETE_GAME = 'delete from game where id = %s'
SQL_SELECT_GAMES = 'SELECT id, name, genre, platform from game'
SQL_SELECT_GAME_BY_ID = 'SELECT id, name, genre, platform from game where id = %s'
SQL_SELECT_USER_BY_ID = 'SELECT id, name, password from user where id = %s'


class GameDAO:
    def __init__(self, db):
        self.__db = db

    def save(self, game):
        cursor = self.__db.connection.cursor()

        if game.id:
            cursor.execute(SQL_UPDATE_GAME, (game.name, game.genre, game.platform, game.id))
        else:
            cursor.execute(SQL_INSERT_GAME, (game.name, game.genre, game.platform))
            game.id = cursor.lastrowid
        self.__db.connection.commit()
        return game

    def list(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SELECT_GAMES)
        games = map_games(cursor.fetchall())
        return games

    def search_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SELECT_GAME_BY_ID, (id,))
        game_tuple = cursor.fetchone()
        return Game(game_tuple[1], game_tuple[2], game_tuple[3], id=game_tuple[0])

    def delete(self, id):
        self.__db.connection.cursor().execute(SQL_DELETE_GAME, (id, ))
        self.__db.connection.commit()


class UserDAO:
    def __init__(self, db):
        self.__db = db

    def search_by_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_SELECT_USER_BY_ID, (id,))
        data = cursor.fetchone()
        user = map_user(data) if data else None
        return user


def map_games(games):
    def create_game_from_tuple(game_tuple):
        return Game(game_tuple[1], game_tuple[2], game_tuple[3], id=game_tuple[0])
    return list(map(create_game_from_tuple, games))


def map_user(user_tuple):
    return User(user_tuple[0], user_tuple[1], user_tuple[2])
