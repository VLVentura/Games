import sqlite3
import os

class Database:
    def __init__(self):
        if 'scoreboard.db' not in os.listdir('db/'):
            conn = sqlite3.connect('db/scoreboard.db')
            cursor = conn.cursor()

            cursor.execute(
                'CREATE TABLE SCOREBOARD ('
                'IDPLAYER INTEGER PRIMARY KEY AUTOINCREMENT,'
                'PLAYERNAME VARCHAR(30) NOT NULL,'
                'SCORE INT NOT NULL'
                ')'
            )

            cursor.close()
            conn.close()

        self.conn = sqlite3.connect('db/scoreboard.db')
        self.cursor = self.conn.cursor()
    
    def insert(self, player, score):
        query = 'INSERT INTO SCOREBOARD (PLAYERNAME, SCORE) VALUES (?, ?)'
        self.cursor.execute(query, (player, score))
        self.conn.commit()
    
    def delete(self):
        query = 'DELETE FROM SCOREBOARD'
        self.cursor.execute(query, ())
        self.conn.commit()
    
    def read(self):
        query = 'SELECT * FROM SCOREBOARD ORDER BY SCORE'
        self.cursor.execute(query)

        readData = []
        for data in self.cursor.fetchall():
            readData.append((data[1], data[2]))
            if len(readData) == 5:
                break
        
        return readData[::-1]
            
    def close(self):
        self.cursor.close()
        self.conn.close()