import sqlite3
import os

class Database:
    def __init__(self):
        if 'database.db' not in os.listdir('db/'):
            conn = sqlite3.connect('db/database.db')
            cursor = conn.cursor()

            cursor.execute(
                'CREATE TABLE SCOREBOARD ('
                'IDPLAYER INTEGER PRIMARY KEY AUTOINCREMENT,'
                'PLAYERNAME VARCHAR(30) NOT NULL,'
                'SCORE INT NOT NULL'
                ')'
            )
            cursor.execute(
                'CREATE TABLE MATCH_HISTORY ('
                'IDMATCH INTEGER PRIMARY KEY AUTOINCREMENT,'
                'PLAYER_ONE_NAME VARCHAR(30) NOT NULL,'
                'PLAYER_ONE_SCORE INT NOT NULL,'
                'PLAYER_TWO_NAME VARCHAR(30) NOT NULL,'
                'PLAYER_TWO_SCORE INT NOT NULL'
                ')'
            )

            cursor.close()
            conn.close()

        self.conn = sqlite3.connect('db/database.db')
        self.cursor = self.conn.cursor()
    
    def insert(self, playerOneName, playerOneScore, playerTwoName, playerTwoScore):
        names = [playerOneName, playerTwoName]
        scores = [playerOneScore, playerTwoScore]
        for i in range(2):
            query = 'INSERT INTO SCOREBOARD (PLAYERNAME, SCORE) VALUES (?, ?)'
            self.cursor.execute(query, (names[i], scores[i]))
            self.conn.commit()
        
        query = 'INSERT INTO MATCH_HISTORY (PLAYER_ONE_NAME, PLAYER_ONE_SCORE, PLAYER_TWO_SCORE, PLAYER_TWO_NAME) VALUES (?, ?, ?, ?)'
        self.cursor.execute(query, (playerOneName, playerOneScore, playerTwoScore, playerTwoName))
        self.conn.commit()
    
    def delete(self, table):
        query = 'DELETE FROM {}'.format(table)
        self.cursor.execute(query)
        self.conn.commit()
    
    def read_from_scoreboard(self):
        query = 'SELECT * FROM SCOREBOARD ORDER BY SCORE'
        self.cursor.execute(query)

        readData = []
        for data in self.cursor.fetchall():
            readData.append((data[1], data[2]))
            if len(readData) == 5:
                break
        
        return readData[::-1]
    
    def read_from_match_history(self):
        query = 'SELECT * FROM MATCH_HISTORY'
        self.cursor.execute(query)

        readData = []
        for data in self.cursor.fetchall():
            readData.append((data[1], data[2], data[3], data[4]))
            if len(readData) == 5:
                break
        
        return readData
            
    def close(self):
        self.cursor.close()
        self.conn.close()