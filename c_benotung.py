from db import DB

class Grade:
    def __init__(self, kidID: int, bookID: int, page: int, grade: int, weight: float, comment: str, date: str):
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
        with DB() as db:
            db.query("INSERT INTO Grade (kidID, bookID, page, grade, comment, weight, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                     (self.kidID, self.bookID, self.page, self.grade, self.comment, self.weight, self.date))

    def update(self):
        with DB() as db:
            db.query("UPDATE Grade SET grade = ?, comment = ?, weight = ?, date = ? WHERE kidID = ? AND bookID = ? AND page = ?",
                     (self.grade, self.comment, self.weight, self.date, self.kidID, self.bookID, self.page))

    def delete(self):
        with DB() as db:
            db.query("DELETE FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (self.kidID, self.bookID, self.page))
