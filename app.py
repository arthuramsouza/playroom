from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config.from_object('config')
db = MySQL(app)

from views import *

if __name__ == '__main__':
    app.run()
