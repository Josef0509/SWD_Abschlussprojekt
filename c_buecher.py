#class definition for handling books
from db import DB

class Book:
    def __init__(self, name:str, pages:int = None, autonumbering:bool = None):
        self.name = name
        self.pages = pages
        self.autonumbering = autonumbering

    def __str__(self):
        return F"Name: {self.name}, Seiten: {self.pages}, Autonumerierung: {self.autonumbering}"
    
    def check_if_book_name_exists(self):
        db = DB()
        ans = db.query("SELECT name FROM Book WHERE name = ?", (self.name,)) != []  #returns True if book exists
        db.__del__()
        return ans

    def save_new_book(self):
        db = DB()
        db.query("INSERT INTO Book (name, pages, autonumbering) VALUES (?, ?, ?)", (self.name, self.pages, self.autonumbering)) == ""
        for i in range(1, self.pages+1):
            db.query("INSERT INTO Assignment (bookID, name) VALUES (?, ?)", (self.get_ID(), i))
        db.__del__()
    
    def update(self, namealt:str):
        db = DB()     
        db.query("UPDATE Book SET name = ?, pages = ?, autonumbering = ? WHERE name = ?", (self.name, self.pages, self.autonumbering, namealt)) == ""
        for i in range(1, self.pages+1):
            ispage = db.query("SELECT * FROM Assignment WHERE bookID = ? AND name = ?", (self.get_ID(), i))
            if ispage == []:
                db.query("INSERT INTO Assignment (bookID, name) VALUES (?, ?)", (self.get_ID(), i))
        db.__del__()

    def delete(self):
        db = DB()
        #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
        db.query("DELETE FROM Book WHERE name = ?", (self.name,)) == ""
        db.__del__()

    def get_ID(self):
        db = DB()
        ans = db.query("SELECT bookID FROM Book WHERE name = ?", (self.name,))
        db.__del__()
        return ans[0][0]
    
    def get_name(self):
        return self.name