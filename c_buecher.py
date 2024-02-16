#class definition for handling books
from db import DB

class Book:
    def __init__(self, name:str, pages:int, autonumbering:bool):
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
        db.__del__()
    
    def update_book(self, namealt:str):
        db = DB()     
        db.query("UPDATE Book SET name = ?, pages = ?, autonumbering = ? WHERE name = ?", (self.name, self.pages, self.autonumbering, namealt)) == ""
        db.__del__()

    def delete_book(self):
        db = DB()
        #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
        db.query("DELETE FROM Book WHERE name = ?", (self.name,)) == ""
        db.__del__()
