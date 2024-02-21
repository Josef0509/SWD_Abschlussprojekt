import sqlite3

class DB:
    def __init__(self):
        self.conn = sqlite3.connect('Notensoftware.db')
        self.c = self.conn.cursor()

    def query(self, query: str, params: tuple = None):
        with self.conn:
            if params:
                self.c.execute(query, params)
            else:
                self.c.execute(query)
            answer = self.c.fetchall()
        return answer
        
    def __del__(self):
        self.conn.close()


    #loads all book-names from the database
    def load_books(self):
        buecher = self.query("SELECT name FROM Book")     #returns tuples
        buecher = [buch[0] for buch in buecher]         #convert to list
        return buecher
    
    #loads all book-data from the database
    def load_book_data(self, name:str):
        data = self.query("SELECT * FROM Book WHERE name = ?", (name,))
        return data

    #loads all kid-names from the database
    def load_kids(self):
        kids = self.query("SELECT firstname, lastname FROM Kid")     #returns tuples
        if kids != []:
            kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list
        return kids
    
    #loads all kid-names from the database, which are in the group with the given groupID or in no group
    def load_kids_in_group_or_available(self, groupID:int):
        kids_in = self.query("SELECT firstname, lastname FROM Kid WHERE groupID = ?", (groupID,))     #returns tuples
        kids_nowhere = self.query("SELECT firstname, lastname FROM Kid WHERE groupID IS NULL")     #returns tuples
        if kids_in != []:
            kids_in = [kid[0]+" "+kid[1] for kid in kids_in]   #convert to list
        if kids_nowhere != []:
            kids_nowhere = [kid[0]+" "+kid[1] for kid in kids_nowhere]   #convert to list
        
        return kids_in, kids_nowhere

    #is used to store username and hashed password in the database
    def save_credentials(self, username:str, password:str):
        self.query("INSERT INTO Credentials (username, password) VALUES (?, ?)", (username, password))
        
    #is used to get the credentials from the database
    def get_credentials(self):
        credentials = self.query("SELECT * FROM Credentials")
        usernames = [credential[0] for credential in credentials]
        passwords = [credential[1] for credential in credentials]
        return usernames, passwords
    
    #loads all group-names from the database
    def load_groups(self):
        groups = self.query("SELECT groupname FROM 'Group'")     #returns tuples
        groups = [group[0] for group in groups]         #convert to list
        return groups
    
    #load group