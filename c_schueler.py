#class definition for handling books
from db import DB

class Kid:
    def __init__(self, firstname:str, lastname:str, groupID:int = None, textfield = None):
        self.firstname = firstname
        self.lastname = lastname
        self.groupID = groupID
        self.textfield = textfield

    def __str__(self):
        return F"Vorname: {self.firstname}, Nachname: {self.lastname}"
    
    def check_if_kid_name_exists(self):
        db = DB()
        ans = bool(db.query("SELECT 1 FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname,self.lastname)))
        db.__del__()
        return ans
    
    def get_name(self):
        return self.firstname +" "+ self.lastname

    def save_new_kid(self):
        db = DB()
        db.query("INSERT INTO Kid (firstname, lastname, groupID) VALUES (?, ?, ?)", (self.firstname, self.lastname, self.groupID)) 
        db.__del__()
    
    def update_name(self, firstname_alt:str, lastname_alt:str):
        db = DB()     
        db.query("UPDATE Kid SET firstname = ?, lastname = ? WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname, firstname_alt, lastname_alt))
        db.__del__()

    def update_group(self, groupID:int):  
        db = DB()     
        db.query("UPDATE Kid SET groupID = ? WHERE firstname = ? AND lastname = ?", (groupID, self.firstname, self.lastname))
        db.__del__() 

    def delete(self):
        db = DB()
        #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
        db.query("DELETE FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname))
        db.__del__()

    def get_kid_ID(self):
        db = DB()
        kidID = db.query("SELECT kidID FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname))
        db.__del__()
        return kidID[0][0]
    
    def get_grades_with_bookID(self, bookID:int):
        db = DB()
        grades = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ?", (self.get_kid_ID(), bookID))
        db.__del__()
        grades = [grade[0] for grade in grades] #unpacking the list of tuples
        return grades
    
    def get_weights_with_bookID(self, bookID:int):
        db = DB()
        weights = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ?", (self.get_kid_ID(), bookID))
        db.__del__()
        weights = [weight[0] for weight in weights]
        return weights
    
    def get_first_last_name(self):
        return self.firstname, self.lastname
    
    def get_textfield(self):
        db = DB()
        textfield = db.query("SELECT textfield FROM Kid WHERE firstname = ? AND lastname = ?", (self.firstname, self.lastname))
        db.__del__()
        return textfield[0][0]
    
    def set_textfield(self, textfield:str):
        db = DB()
        self.textfield = textfield
        db.query("UPDATE Kid SET textfield = ? WHERE firstname = ? AND lastname = ?", (self.textfield, self.firstname, self.lastname))
        db.__del__()