from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog
import datetime
from c_gruppen import Group


# Configuration of the page
st.set_page_config(layout="wide", page_title="Benotung", page_icon=":1234:")

# Add title to the page
st.title(":1234:"+" Benotung")


# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1


# Add columns for buttons
cl1, cl2, cl3 = st.columns([0.3, 1, 1])

# Add buttons to the page
button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1),
                         help="Klicken Sie hier um zur Übersicht zu gelangen!")

button2_ph = cl2.button("Detailansicht", on_click=lambda: st.session_state.__setitem__("showSession", 2),
                        help="Klicken Sie hier um die Detailansicht zu sehen!")




# Add a container to the page
container = st.container()

# Create a database object
db = DB()

try:
    # Load all book-names from the database
    buecher = db.query("SELECT name FROM Book")  # returns tuples
    buecher = [buch[0] for buch in buecher] if buecher else []

except Exception as e:
    st.text("Keine Bücher vorhanden!")


# Create a selectbox to select a book
selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")




#++++++++++++++++++++++++++++++++++ÜBERSICHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def uebersicht():

    # Create a database object
    try:
        db = DB()
    except Exception as e:
        st.text("Fehler bei der Verbindung mit der Datenbank!")
    #visual appearance
        
    container.divider()
    st.header("Benotungsübersicht:")

    
    #sessionstate variables to selected book
    selected_book = st.session_state.key_ausg_Buch
    
    try: 
        #get the number of pages of the selected book
        seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
        seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None
    except Exception as e:
        st.text("Fehler bei der Übergabe der Seitenanzahl des Buches!")

    try:
        #get the book_id of the selected book
        book_id = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
        book_id = book_id[0][0]
    except Exception as e:
        st.text("Fehler bei der Übergabe der BuchID des Buches!") 
  
    if seitenanz_aus_DB:
       
        #load all groups from the database
        try:
            groups = db.load_groups()
        except Exception as e:
            st.write("Fehler bem Laden der Gruppen!")

        for group in groups:
            
            #create a dataframe for each group
            df_group = pd.DataFrame()

            try:
                #get the group_id of the selected group
                group_id = Group(group).get_groupID()
            except Exception as e:
                st.write("Fehler beim Laden der GruppenID!")
           

            try:
                #get the kids in the selected group
                kids_in_group, kids_nowhere = db.load_kids_in_group_or_available(group_id)
            except:
                st.write("Fehler beim Laden der Kinder in der Gruppe!")

            try:
                #get the kid_ids of the kids in the selected group
                kid_ids = db.query("SELECT kidID FROM Kid WHERE groupID = ?", (group_id,))
            except Exception as e:
                st.write("Fehler beim Laden der KidID")

            #create a new column for each page of the selected book
            for page in range(1, seitenanz_aus_DB + 1):

                page_grades = []


                #get the grades of the kids in the selected group for each page
                for kid_id in kid_ids:
                    
                    try:
                        grade = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id[0], book_id, page))
                    except Exception as e:
                        st.write("Fehler beim Laden der Noten!")

                    #if grade is present, append it to the list, else append an empty string
                    if grade:
                        page_grades.append(grade[0][0])
                    else:
                        page_grades.append("")
                
                #add the list of grades to the dataframe
                df_group[f"S. {page}"] = page_grades
            
            #insert the kid names as the first column
            df_group.insert(0, 'Kid Name', kids_in_group)  # Insert Kid Names as the first column


            #visual appearance
            st.subheader(group)

            #display the dataframe
            st.data_editor(
                    df_group,
                    hide_index=True,
                    disabled=df_group.columns,
                )
            st.caption(f"Hier sehen Sie die Noten der Kinder in der {group} für das Fach {selected_book}.")



            #export the dataframe to a csv file

            #create file path for each group
            file_path = f"C:\\Users\\sandr\\OneDrive\\Desktop\\test\\{group}_export.csv"

            try:

                #create a button to export the dataframe to a csv file
                if st.button(f"Export {group} to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):
                    df_group.to_csv(file_path, sep='\t')
                    st.success(f"Data successfully exported to {file_path}")

            except Exception as e:
                st.write("Fehler beim Exportieren als CSV!")

            #visual appearance
            st.divider()
        
        #visual appearance
        st.caption("Die Spalten entsprechen den Seiten des Buches und die Zeilen den Kindern. Die Noten sind in den Zellen eingetragen. Wenn eine Zelle leer ist, hwurde die Seite noch nicht bewertet.")

            
    else:
        container.write("Das Buch hat keine Seitenanzahl.")

    return 
            
    


#++++++++++++++++++++++++++++++++++DETAILANSICHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def detailansicht():
    #database object
    db = DB()


    #group selection
    selected_group = container.selectbox(label="Gruppe auswählen", key="key_ausg_Gruppe", index=0, options=db.load_groups(),
                                            help="Bitte hier die Gruppe auswählen die Sie anzeigen wollen!")
    
    group_id = Group(selected_group).get_groupID()


    #kid selection
    kids_in_group, kids_nowhere = db.load_kids_in_group_or_available(group_id)
    
    selected_kid = container.selectbox(label="Kind auswählen", key="key_ausg_Kind", index=0, options=kids_in_group,
                                            help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    
    #get kid names
    first_name = selected_kid.split(" ")[0]
    last_name = selected_kid.split(" ")[1]
    
    #get kid_id
    kid_id = db.query("SELECT kidID FROM Kid WHERE firstname = ? AND lastname = ?", (first_name, last_name,))
    kid_id = kid_id[0][0]
    

    #book selection
    book_id_result = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
    book_id = book_id_result[0][0]
    


    #count how many pages are already graded

    #count_pages = db.query("SELECT COUNT(DISTINCT page) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
    #count_pages = count_pages[0][0] if count_pages and count_pages[0] else None
    #st.header(count_pages)

    #if count_pages == 0:
    #    count_pages = 1
    
    #get the number of pages of the selected book
    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None
    

    #select first ungraded page
    last_graded_page = db.query("SELECT MAX(page) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
    last_graded_page = last_graded_page[0][0] 
    if last_graded_page == None:
        last_graded_page = 1

    #page selection, +1 for next page to grade
    selected_page = container.number_input(label="Seite auswählen", key="key_ausg_Seite", value=last_graded_page+1, placeholder="Seite", help="Bitte hier die Seite auswählen die Sie anzeigen wollen!", step=1, min_value=1, max_value=seitenanz_aus_DB)
    
 
    #get the grade, comment, weight and date of the selected page
    grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id,selected_page))
    
    comment_result = db.query("SELECT comment FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    
    weight_result = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    
    date_result = db.query("SELECT date FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
    

    #visual appearance
    st.divider()
    st.header("Eingabe der Details:")



    #------------------------INPUTS---------------------------------------------------------------------
    #if no grade is present, set grade_result to 1
    if grade_result==[]:
        grade_result = 1
    else:
        grade_result = grade_result[0][0]
    #input for grade
    st.number_input(label = "Note", key="key_grade_input", value=grade_result, placeholder="Note", help="Bitte hier die Note eintragen!", step=1, min_value=1, max_value=5)
    

    #if no comment is present, set comment_result to None
    if comment_result==[]:
        comment_result = ""
    else:
        comment_result = comment_result[0][0]
    #input for comment
    st.text_input(label="Kommentar", placeholder="Kommentar", help="Bitte hier ihren Kommentar eingeben", key="key_comment_input",value=comment_result)
    

    #if no weight is present, set weight_result to 0.0
    if weight_result==[]:
        weight_result = 0.0
    else:
        weight_result = weight_result[0][0]
    #input for weight
    st.number_input(label = "Gewichtung", key="key_weight_input", value=weight_result, placeholder="Gewichtung", help="Bitte hier die Gewichtung eintragen!", step=1.0, min_value=0.0, max_value=100.0)
    

    #if no date is present, set date_result to today's date
    if date_result == []:
        date_result = datetime.date.today()

    else:
        # Extract the date string from the tuple
        date_result = date_result[0][0]
        date_string = date_result
        # Convert the date string to a datetime.date object
        date_result = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()

    #input for date
    st.date_input(label="Datum", help="Bitte hier das Datum eingeben", key="key_date_input", value=date_result)


    #------------------------BUTTONS---------------------------------------------------------------------
    #buttons for saving, updating and deleting the grade
    button_col1, button_col2, button_col3 = st.columns([0.3, 1, 1])


    if button_col1.button("Speichern", help="Klicken Sie hier um die Note zu speichern!"):
        grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
        if grade_result:
            db.query("UPDATE Grade SET grade = ?, comment = ?, weight = ?, date = ? WHERE kidID = ? AND bookID = ? AND page = ?", (st.session_state.key_grade_input, st.session_state.key_comment_input, st.session_state.key_weight_input, st.session_state.key_date_input, kid_id, book_id, selected_page))
            st.success("Erfolgreich geupdated")
        else:
            db.query("INSERT INTO Grade (kidID, bookID, page, grade, comment, weight, date) VALUES (?, ?, ?, ?, ?, ?, ?)", (kid_id, book_id, selected_page, st.session_state.key_grade_input, st.session_state.key_comment_input, st.session_state.key_weight_input, st.session_state.key_date_input))
            st.success("Note erfolgreich gespeichert!")

        

    if button_col2.button("Löschen", help="Klicken Sie hier um die Note zu löschen!"):
        db.query("DELETE FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
        st.success("Erfolgreich gelöscht")






#----------------------------SESSIONSTATES------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()

elif st.session_state.showSession == 2:
    detailansicht()

else:
    pass
