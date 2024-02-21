from db import DB

class Grade:
    def __init__(self, kidID: int, bookID: int, page: int, grade: int = None, weight: float = None, comment: str = None, date: str = None):
        self.kidID = kidID
        self.bookID = bookID
        self.page = page
        self.grade = grade
        self.weight = weight
        self.comment = comment
        self.date = date

    def __str__(self):
        return f"KidID: {self.kidID}, BookID: {self.bookID}, Page: {self.page}, Grade: {self.grade}, Weight: {self.weight}, Comment: {self.comment}, Date: {self.date}"

    def save_new_grade(self):
        db = DB()
        db.query("INSERT INTO Grade (kidID, bookID, page, grade, comment, weight, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (self.kidID, self.bookID, self.page, self.grade, self.comment, self.weight, self.date))
        db.__del__()

    def update(self):
        db = DB()
        db.query("UPDATE Grade SET grade = ?, comment = ?, weight = ?, date = ? WHERE kidID = ? AND bookID = ? AND page = ?",
                     (self.grade, self.comment, self.weight, self.date, self.kidID, self.bookID, self.page))
        db.__del__()

    def delete(self):
        db = DB()
        db.query("DELETE FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (self.kidID, self.bookID, self.page))
        db.__del__()

    def get_grade(self):
        db = DB()
        grade = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (self.kidID, self.bookID, self.page))
        db.__del__()
        return grade                   
