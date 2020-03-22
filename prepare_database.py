import MySQLdb
print('Connecting...')
conn = MySQLdb.connect(user='root', passwd='admin', host='127.0.0.1', port=3306)

# Drop database
conn.cursor().execute("DROP DATABASE `playroom`;")
conn.commit()

# Create database and its tables
create_tables = '''SET NAMES utf8;
    CREATE DATABASE `playroom` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_bin */;
    USE `playroom`;
    CREATE TABLE `game` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `name` varchar(50) COLLATE utf8_bin NOT NULL,
      `genre` varchar(40) COLLATE utf8_bin NOT NULL,
      `platform` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE `user` (
      `id` varchar(8) COLLATE utf8_bin NOT NULL,
      `name` varchar(20) COLLATE utf8_bin NOT NULL,
      `password` varchar(8) COLLATE utf8_bin NOT NULL,
      PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;'''

conn.cursor().execute(create_tables)

# Inserting users
cursor = conn.cursor()
cursor.executemany(
      'INSERT INTO playroom.user (id, name, password) VALUES (%s, %s, %s)',
      [
            ('arthur', 'Arthur Menezes', '1234'),
            ('admin', 'Admin', 'admin'),
            ('masterchief', 'John-117', 'cortana')
      ])

cursor.execute('select * from playroom.user')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# Inserting games
cursor.executemany(
      'INSERT INTO playroom.game (name, genre, platform) VALUES (%s, %s, %s)',
      [
            ('Halo 2', 'Sci-fi', 'Xbox'),
            ('Red Dead Redemption', 'Action', 'Xbox 360'),
            ('NBA 2k18', 'Esporte', 'Xbox One'),
            ('Rayman Legends', 'Indie', 'PS4'),
            ('Super Mario RPG', 'RPG', 'SNES'),
            ('Super Mario Kart', 'Corrida', 'SNES'),
            ('Fire Emblem Echoes', 'Estratégia', '3DS'),
      ])

cursor.execute('select * from playroom.game')
print(' -------------  Games:  -------------')
for game in cursor.fetchall():
    print(game[1])

# Committing and closing
conn.commit()
cursor.close()
