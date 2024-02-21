#class definition for handling books
from db import DB

class Kid:
    def __init__(self, firstname:str, lastname:str):
        self.firstname = firstname
        self.lastname = lastname

    def __str__(self):
        return F"Vorname: {self.firstname}, Nachname: {self.lastname}"
    
    def check_if_kid_name_exists(self):
        db = DB()
        ans = bool(db.query("SELECT 1 FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname,self.lastname)))
        db.__del__()
        return ans

    def save_new_kid(self):
        db = DB()
        db.query("INSERT INTO Kid (firstname, lastname, groupID) VALUES (?, ?, ?)", (self.firstname, self.lastname, 1)) #groupID TBD
        db.__del__()
    
    def update(self, firstname_alt:str, lastname_alt:str):
        db = DB()     
        db.query("UPDATE Kid SET firstname = ?, lastname = ? WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname, firstname_alt, lastname_alt))
        db.__del__()

    def delete(self):
        db = DB()
        #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
        db.query("DELETE FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname))
        db.__del__()