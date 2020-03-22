class Game:
    def __init__(self, name, genre, platform, id=None):
        self.id = id
        self.name = name
        self.genre = genre
        self.platform = platform


class User:
    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password
