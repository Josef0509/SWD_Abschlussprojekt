from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog
import datetime

st.set_page_config(layout="wide", page_title="Benotung", page_icon=":1234:")
st.title(":1234:"+" Benotung")


# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

cl1, cl2, cl3 = st.columns([0.3, 1, 1])
button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1),
                         help="Klicken Sie hier um zur Übersicht zu gelangen!")

button2_ph = cl2.button("Detailansicht", on_click=lambda: st.session_state.__setitem__("showSession", 2),
                        help="Klicken Sie hier um die Detailansicht zu sehen!")





container = st.container()
db = DB()


buecher = db.query("SELECT name FROM Book")  # returns tuples
buecher = [buch[0] for buch in buecher] if buecher else []

selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                    help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")




#wenn Gruppen fertig sind dann hier einfügen
#groups = db.query("SELECT groupname FROM Group")  # returns tuples
#selected_group = container.selectbox(label="Gruppe auswählen", key="key_ausg_Gruppe", index=0, options=groups,
#                                     help="Bitte hier die Gruppe auswählen die Sie anzeigen wollen!")

#selected_group_id = db.query("SELECT groupID FROM Group WHERE groupname = ?", (selected_group,))



# ------------------------------------------------------------------------------------------------------------------------------
def uebersicht():
    st.header("Benotungsübersicht")
    db = DB()

    selected_book = st.session_state.key_ausg_Buch
    
    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None

    book_id = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
    book_id = book_id[0][0]
        

    kids = db.query("SELECT firstname, lastname FROM Kid " )     #returns tuples

    if kids != []: 
         kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list

    df = pd.DataFrame()

    if seitenanz_aus_DB:
       # container.write(f"Seitenanzahl: {seitenanz_aus_DB}")

        # Fetch all kidIDs
        kid_ids = db.query("SELECT kidID FROM Kid")
        #container.write(kid_ids)

        for page in range(1, seitenanz_aus_DB + 1):
            page_grades = []

            for kid_id in kid_ids:
                #mache eine neue spalte für die noten von dieer seite
                grade = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id[0], book_id, page))
                if grade:
                    page_grades.append(grade[0][0])
                else:
                    page_grades.append(None)
                
            df[f"S. {page}"] = page_grades

        df.insert(0, 'Kid Name', kids)  # Insert Kid Names as the first column




        # Get dataframe row-selections from user with st.data_editor
        st.data_editor(
            df,
            hide_index=True,
            disabled=df.columns,
        )

        
        

        


        # Open file explorer for user to choose file path
        file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

        # Export the DataFrame to the specified file path
        if st.button("Export to CSV"):
            df.to_csv(file_path, sep='\t')
            st.success(f"Data successfully exported to {file_path}")


    else:
        container.write("Das Buch hat keine Seitenanzahl.")

    return 
            
    




#--------------------------------------------------------------------------------------------------------------------------------------
def detailansicht():
    db = DB()


    #book_id = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
    #book_id = book_id[0][0]


    kids = db.query("SELECT firstname, lastname FROM Kid " )     #returns tuples

    if kids != []: 
         kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list

    selected_kid = container.selectbox(label="Kind auswählen", key="key_ausg_Kind", index=0, options=kids,
                                            help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    
    #st.write("selected_kid")
    #st.header(selected_kid)
    first_name = selected_kid.split(" ")[0]
    last_name = selected_kid.split(" ")[1]
    

    kid_id = db.query("SELECT kidID FROM Kid WHERE firstname = ? AND lastname = ?", (first_name, last_name,))
    kid_id = kid_id[0][0]
    #st.write("kid_id")
    #st.header(kid_id)


    book_id_result = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
    book_id = book_id_result[0][0]
    #st.write("Book_id")
    #st.header(book_id)



    
    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None
    


    #count how many pages are already graded

    #count_pages = db.query("SELECT COUNT(DISTINCT page) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
    #count_pages = count_pages[0][0] if count_pages and count_pages[0] else None
    #st.header(count_pages)

    #if count_pages == 0:
    #    count_pages = 1


    #select first ungraded page
    last_graded_page = db.query("SELECT MAX(page) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
    last_graded_page = last_graded_page[0][0] if last_graded_page and last_graded_page[0] else None
    #st.header(last_graded_page)


    selected_page = container.number_input(label="Seite auswählen", key="key_ausg_Seite", value=last_graded_page, placeholder="Seite", help="Bitte hier die Seite auswählen die Sie anzeigen wollen!", step=1, min_value=1, max_value=seitenanz_aus_DB)
    
    
    
    
    

    

    grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id,selected_page))
    #st.write("Grade")
    #st.header(grade_result)

    comment_result = db.query("SELECT comment FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    #st.write("Comment")
    #st.header(comment_result)

    weight_result = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    #st.write("Weight")
    #st.header(weight_result)

    date_result = db.query("SELECT date FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    #st.write("Date")
    #st.header(date_result)


    
    st.header("Eingabe der Details:")

    #INPUTS

    if grade_result==[]:
        grade_result = 1
    else:
        grade_result = grade_result[0][0]

    st.number_input(label = "Note", key="key_grade_input", value=grade_result, placeholder="Note", help="Bitte hier die Note eintragen!", step=1, min_value=1, max_value=5)
    

    
    if comment_result==[]:
        comment_result = None
    else:
        comment_result = comment_result[0][0]
    st.text_input(label="Kommentar", placeholder="Kommentar", help="Bitte hier ihren Kommentar eingeben", key="key_comment_input",value=comment_result)
    

    if weight_result==[]:
        weight_result = 0.0
    else:
        weight_result = weight_result[0][0]
    st.number_input(label = "Gewichtung", key="key_weight_input", value=weight_result, placeholder="Gewichtung", help="Bitte hier die Gewichtung eintragen!", step=1.0, min_value=0.0, max_value=100.0)
    


    if date_result == []:
        # If nothing is present, set today's date
        date_result = datetime.date.today()
        #convert in datetime.date object
        #st.header(date_result)

    else:
        # Extract the date string from the tuple
        date_result = date_result[0][0]
        date_string = date_result
        #st.header(date_string)
        # Convert the date string to a datetime.date object
        date_result = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    # Now use date_input with the modified date_result
    st.date_input(label="Datum", help="Bitte hier das Datum eingeben", key="key_date_input", value=date_result)



    button_col1, button_col2, button_col3 = st.columns(3)


    if button_col3.button("Speichern"):
        db.query("INSERT INTO Grade (kidID, bookID, page, grade, comment, weight, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (kid_id, book_id, selected_page, st.session_state.key_grade_input, st.session_state.key_comment_input, st.session_state.key_weight_input, st.session_state.key_date_input))
        st.success("Note erfolgreich gespeichert!")


    if button_col1.button("Updaten"):
        db.query("UPDATE Grade SET grade = ?, comment = ?, weight = ?, date = ? WHERE kidID = ? AND bookID = ? AND page = ?", (st.session_state.key_grade_input, st.session_state.key_comment_input, st.session_state.key_weight_input, st.session_state.key_date_input, kid_id, book_id, selected_page))
        st.success("Erfolgreich geupdated")

    if button_col2.button("Löschen"):
        db.query("DELETE FROM Grade WHERE kidID = ?", (kid_id,))
        st.success("Erfolgreich gelöscht")


        
        

        







        





#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()

elif st.session_state.showSession == 2:
    detailansicht()

else:
    pass
