from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from datetime import datetime
from tkinter import filedialog

class Benotung():
    db=DB()


    #Konstruktor
    def __init__(self, buchID : int, kidID : int, gradeID : int, page : int, grade : int, weight : float,  comment : str, date : datetime):
        self.buchid = buchID
        self.kidid = kidID
        self.gradeid = gradeID
        self.page = page
        self.grade = grade
        self.weight = weight
        self.comment = comment
        self.date = date


    
    def __str__(self) -> str:
        return f"BuchID: {self.buchid}, KidID: {self.kidid}, GradeID: {self.gradeid}, Page: {self.page}, Grade: {self.grade}, Weight: {self.weight}, Comment: {self.comment}, Date: {self.date}"
    
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def save(self):
        # Saving to the SQLite database
        

        values = (
            self.kidid,
            self.buchid,
            self.gradeid,  
            self.page,
            self.grade,
            self.weight,
            self.comment,
            self.date
        )

        self.db.query("INSERT INTO GRADE (kidID, bookID, gradeID, page, grade, weight, comment, date) VALUES (?, ?, ?, ?, ?, ?, ?)", values)