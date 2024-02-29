#class definition for handling books
from db import DB

class Group:
    def __init__(self, name:str):
        self.name = name

    def __str__(self):
        return F"Group: {self.name}"
    
    def check_if_group_exists(self):
        db = DB()
        ans = db.query("SELECT groupID FROM 'Group' WHERE groupname = ?", (self.name,)) != []
        db.__del__()
        return ans

    def save_new_group(self):
        db = DB()
        db.query("INSERT INTO 'Group' (groupname) VALUES (?)", (self.name,))
        db.__del__()
    
    def update(self, new_name:str):
        db = DB()     
        db.query("UPDATE 'Group' SET groupname = ? WHERE groupname = ?", (new_name, self.name))
        self.name = new_name
        db.__del__()

    def delete(self):
        db = DB()
        #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
        db.query("DELETE FROM 'Group' WHERE groupname = ?", (self.name,))
        db.__del__()

    def get_groupID(self):
        db = DB()
        ans = db.query("SELECT groupID FROM 'Group' WHERE groupname = ?", (self.name,))
        db.__del__()
        if ans == []:
            return None
        else:
            return ans[0][0]
