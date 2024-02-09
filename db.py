import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Notensoftware.db')
        self.c = self.conn.cursor()

    def query(self, query:str, params:tuple = None):
        if params:
            self.c.execute(query, params)
        else:
            self.c.execute(query)
        self.conn.commit()
        answer = self.c.fetchall()
        return answer
    
    def __del__(self):
        self.conn.close()
        
