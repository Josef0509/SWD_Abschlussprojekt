from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog
import datetime
from c_gruppen import Group
import logging
from c_benotung import gradeTOPercentage, percentageTOGrade
from c_schueler import Kid
from c_buecher import Book
import os
import pdfkit
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


#configure logfile
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')
logging.info('Benotung ausgewaehlt')


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
    logging.exception('Fehler beim Laden der Bücher!')
    st.text("Fehler beim Laden der Bücher!")


# Create a selectbox to select a book
selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")

db.__del__()


#++++++++++++++++++++++++++++++++++ÜBERSICHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def uebersicht():
    logging.info('Übersicht ausgewählt')

    # Create a database object
    try:
        db = DB()
    except Exception as e:
        logging.exception('Fehler beim Laden der Datenbank!')
        st.text("Fehler beim Laden der Datenbank!")
    #visual appearance
        
    container.divider()
    st.header("Benotungsübersicht:")

    
    #sessionstate variables to selected book
    selected_book = st.session_state.key_ausg_Buch
    selected_book = Book(selected_book)
    selected_book_ID = selected_book.get_ID()
    
    try: 
        #get the number of pages of the selected book
        assignmentIDs = db.get_assignment_IDs(selected_book_ID)
        
    except Exception as e:
        logging.exception('Fehler bei der Übergabe der Seitenanzahl des Buches!')
        st.text("Fehler bei der Übergabe der Seitenanzahl des Buches!")

    df_all = pd.DataFrame()


    if assignmentIDs:

       
        #load all groups from the database
        try:
            groups = db.load_groups()
        except Exception as e:
            logging.exception('Fehler beim Laden der Gruppen!')
            st.write("Fehler bem Laden der Gruppen!")

        for group in groups:
            
            #create a dataframe for each group
            df_group = pd.DataFrame()

            try:
                #get the group_id of the selected group
                group_id = Group(group).get_groupID()
            except Exception as e:
                logging.exception('Fehler beim Laden der GruppenID!')
                st.write("Fehler beim Laden der GruppenID!")
           

            try:
                #get the kids in the selected group
                kids_in_group, kids_nowhere = db.load_kids_in_group_or_available(group_id)
            except:
                logging.exception('Fehler beim Laden der Kinder in der Gruppe!')
                st.write("Fehler beim Laden der Kinder in der Gruppe!")

            try:
                #get the kid_ids of the kids in the selected group
                kid_ids = db.query("SELECT kidID FROM Kid WHERE groupID = ?", (group_id,))
            except Exception as e:
                logging.exception('Fehler beim Laden der KidID!')
                st.write("Fehler beim Laden der KidID")

            #create a new column for each page of the selected book
            for assignmentID in assignmentIDs:

                page_grades = []
                assignmentName = db.query("SELECT name FROM Assignment WHERE assignmentID = ?", (assignmentID,))
                assignmentName = assignmentName[0][0] if assignmentName and assignmentName[0] else None


                #get the grades of the kids in the selected group for each page
                for kid_id in kid_ids:
                    
                    try:
                        grade = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND assignmentID = ?", (kid_id[0], selected_book_ID, assignmentID))
                    except Exception as e:
                        logging.exception('Fehler beim Laden der Noten!')
                        st.write("Fehler beim Laden der Noten!")

                    try:
                        #if grade is present, append it to the list, else append an empty string
                        if grade:
                            page_grades.append(grade[0][0])
                        else:
                            page_grades.append("")
                    except Exception as e:
                        st.write("Fehler beim hinzuügen der Noten an den list!")
                
                #add the list of grades to the dataframe
                try:
                    df_group[assignmentName] = page_grades
                except Exception as e:
                    st.write("Fehler beim hinzufügen der Noten an das DataFrame!")
            
            #insert the kid names as the first column
            df_group.insert(0, 'Kid Name', kids_in_group)  # Insert Kid Names as the first column


            #visual appearance
            st.subheader(group)

            try:
                #display the dataframe
                st.data_editor(
                    df_group,
                    hide_index=True,
                    disabled=df_group.columns,
                )
            except Exception as e:
                logging.exception('Fehler beim Anzeigen des DataFrames!')
                st.write("Fehler beim Anzeigen des DataFrames!")
            selected_book_name = selected_book.get_name()
            st.caption(f"Hier sehen Sie die Noten der Kinder in der {group} für das Fach: {selected_book_name}.")

            #hänge df_group an df_all an
            #before appending df_group to df_all make one row for the group name
            #row not column

            df_group_for_all = df_group.copy()

            df_group_for_all.insert(0, "Group", group)

            df_all = pd.concat([df_all, df_group_for_all], ignore_index=True)
            
            #get file path from user
            file_path = os.path.join(os.path.expanduser("~"), "Desktop")
            


            try:
                #create a button to export the dataframe to a csv file
                if st.button(f"Export {group} to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):
                    

                    selected_book = selected_book.get_name()
                    time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                    df_group.to_csv(os.path.join(file_path, f"{group}_{selected_book}_{time}grades.csv"), index=False)
                    st.success(f"Data successfully exported to {file_path}")

                    #seite neu laden
                    st.experimental_rerun()

            except Exception as e:
                logging.exception('Fehler beim Exportieren als CSV!')
                st.write("Fehler beim Exportieren als CSV!")

            #visual appearance
            st.divider()
        
        #visual appearance
        st.caption("Die Spalten entsprechen den Seiten des Buches und die Zeilen den Kindern. Die Noten sind in den Zellen eingetragen. Wenn eine Zelle leer ist, hwurde die Seite noch nicht bewertet.")

        st.data_editor(
            df_all,
            hide_index=True,
            disabled=df_all.columns,
        )

        #dataframe als pdf exportieren
        

        #export dataframe to csv
        try:
            if st.button("Export all to CSV", help="Klicken Sie hier um die Daten als CSV zu exportieren!"):


                selected_book = selected_book.get_name()
                time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

                df_all.to_csv(os.path.join(file_path, f"{selected_book}_{time}grades.csv"), index=False)
                st.success(f"Data successfully exported to {file_path}")

                #seite neu laden
                st.experimental_rerun()
        except Exception as e:
            logging.exception('Fehler beim Exportieren als CSV!')
            st.write("Fehler beim Exportieren als CSV!")

        
       

        
        

        try:
            if st.button("Export all to PDF", help="Klicken Sie hier um die Daten als PDF zu exportieren!"):
                
                # Specify the file path for the PDF export
                selected_book = selected_book.get_name()
                time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                output_pdf_path = os.path.join(file_path, f"{selected_book}_{time}grades.pdf")
                pdf = SimpleDocTemplate(output_pdf_path, pagesize=letter)

                # Convert the DataFrame to a list of lists for the Table
                data = [df_all.columns.tolist()] + df_all.values.tolist()
                table = Table(data)

                # Define the style of the table
                #each row has lines
                table_style = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    # ... (your other styles)
                ])

                table.setStyle(table_style)

                # Include the table in the PDF
                elements = [table]

                # Include HTML content in the PDF
                #html_content = "<h1>Hello, this is HTML content</h1>"
                #html_flowable = Paragraph(html_content, getSampleStyleSheet()['Heading1'])
                #elements.append(html_flowable)

                pdf.build(elements)
                st.success(f"Data successfully exported to {output_pdf_path}")
        except Exception as e:
            st.exception('Fehler beim Exportieren als PDF!')
            st.write("Fehler beim Exportieren als PDF!")




            
    else:
        container.write("Das Buch hat keine Seitenanzahl.")

    db.__del__()
    return 
            
    


#++++++++++++++++++++++++++++++++++DETAILANSICHT+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def detailansicht():
    #database object
    try:
        db = DB()
    except Exception as e:
        logging.exception('Fehler beim Laden der Datenbank!')
        st.write("Fehler beim Laden der Datenbank!")


    #group selection
    selected_group = container.selectbox(label="Gruppe auswählen", key="key_ausg_Gruppe", index=0, options=db.load_groups(),
                                            help="Bitte hier die Gruppe auswählen die Sie anzeigen wollen!")
    
    try:

        group_id = Group(selected_group).get_groupID()
    except Exception as e:
        logging.exception('Fehler beim Laden der GruppenID!')
        st.write("Fehler beim Laden der GruppenID!")

    
    try:
        #kid selection
        kids_in_group, kids_nowhere = db.load_kids_in_group_or_available(group_id)
    except Exception as e:
        logging.exception('Fehler beim Laden der Kinder in der Gruppe!')
        st.write("Fehler beim Laden der Kinder in der Gruppe!")
    
    if kids_in_group == []:
        st.error("Es sind keine Kinder in dieser Gruppe.")
        
    else:


        selected_kid = container.selectbox(label="Kind auswählen", key="key_ausg_Kind", index=0, options=kids_in_group,
                                                help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
        
        

        #get kid names
        first_name = selected_kid.split(" ")[0]
        last_name = selected_kid.split(" ")[1]
        
        try:
            #get kid_id
            kid_id = db.query("SELECT kidID FROM Kid WHERE firstname = ? AND lastname = ?", (first_name, last_name,))
            kid_id = kid_id[0][0]
        except Exception as e:
            logging.exception('Fehler beim Laden der KidID!')
            st.write("Fehler beim Laden der KidID!")
        
        
        try:#book selection
            book_id_result = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
            book_id = book_id_result[0][0]
        except Exception as e:
            logging.exception('Fehler beim Laden der BuchID!')
            st.write("Fehler beim Laden der BuchID!")
        


        #count how many pages are already graded

        #count_pages = db.query("SELECT COUNT(DISTINCT page) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
        #count_pages = count_pages[0][0] if count_pages and count_pages[0] else None
        #st.header(count_pages)

        #if count_pages == 0:
        #    count_pages = 1
        
        try:
            #get the number of pages of the selected book
            seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
            seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None
        except Exception as e:
            logging.exception('Fehler bei der Übergabe der Seitenanzahl des Buches!')
            st.write("Fehler bei der Übergabe der Seitenanzahl des Buches!")
        

        try:
            #select first ungraded page
            last_graded_page = db.query("SELECT MAX(assignmentID) FROM Grade WHERE kidID = ? AND bookID = ?", (kid_id, book_id))
            last_graded_page = last_graded_page[0][0] 
            if last_graded_page == None:
                last_graded_page = 1

            #größer als seitananzahl
            if last_graded_page + 1 > seitenanz_aus_DB:
                last_graded_page = seitenanz_aus_DB-1
        except Exception as e:
            logging.exception('Fehler beim Laden der letzten bewerteten Seite!')
            st.write("Fehler beim Laden der letzten bewerteten Seite!")

        #page selection, +1 for next page to grade
        selected_assignment_name = container.text_input(label="Seite auswählen", key="key_ausg_Seite", value=last_graded_page+1, placeholder="Seite", help="Bitte hier die Seite auswählen die Sie anzeigen wollen!")
        




        try:
            #get all assignment names of the selected book
            assignment_names = db.query("SELECT name FROM Assignment WHERE bookID = ?", (book_id,))
            assignment_names = [assignment[0] for assignment in assignment_names] if assignment_names else []

            if selected_assignment_name not in assignment_names:
                st.write("Die Seite existiert nicht.")
                st.button("Aufgabe hinzufügen", help="Klicken Sie hier um eine neue Aufgabe hinzuzufügen!", key="key_add_assignment")
                if st.session_state.key_add_assignment:
                    db.query("INSERT INTO Assignment (bookID, name) VALUES (?, ?)", (book_id, selected_assignment_name))
                    st.experimental_rerun()
            
            assignment_ID = db.query("SELECT assignmentID FROM Assignment WHERE bookID = ? AND name = ?", (book_id, selected_assignment_name))
            assignment_ID = assignment_ID[0][0] if assignment_ID and assignment_ID[0] else None
                    
        except Exception as e:
            logging.exception('Fehler beim Laden der Aufgaben!')
            st.write("Fehler beim Laden der Aufgaben!")
            



        try:
            #get the grade, comment, weight and date of the selected page

            assignment_description = db.query("SELECT description FROM Assignment WHERE assignmentID = ?", (assignment_ID,))

            grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND assignmentID = ?", (kid_id, book_id,assignment_ID))
            
            comment_result = db.query("SELECT comment FROM Grade WHERE kidID = ? AND bookID = ? AND assignmentID = ?", (kid_id, book_id, assignment_ID))
            
            weight_result = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ? AND assignmentID = ?", (kid_id, book_id, assignment_ID))
            
            date_result = db.query("SELECT date FROM Grade WHERE kidID = ? AND bookID = ? AND assignmentID = ?", (kid_id, book_id, assignment_ID))
        except Exception as e:
            logging.exception('Fehler beim Laden der Noten, Kommentare usw.!')
            st.write("Fehler beim Laden der Noten, Kommentare usw.!")
        

        #visual appearance
        st.divider()
        st.header("Eingabe der Details:")



        #------------------------INPUTS---------------------------------------------------------------------
        
        if assignment_description==[]:
            assignment_description = ""
        else:
            assignment_description = assignment_description[0][0]
        #input for assignment description
            
        st.text_area(label="Aufgabenbeschreibung", placeholder="Aufgabenbeschreibung", help="Bitte hier die Aufgabenbeschreibung eingeben", key="key_assignment_description_input", value=assignment_description)



        #if no grade is present, set grade_result to 1
        if grade_result==[]:
            grade_result = "1"
        else:
            grade_result = grade_result[0][0]
        #input for grade
        
        st.toggle(label="Krank", key="key_K_input", value=False, help="Klicken Sie hier wenn das Kind krank war!")

        if st.session_state.key_K_input == False:
            if grade_result == "K":
                grade_result = 1
            st.number_input(label = "Note", key="key_grade_input", value=int(grade_result), placeholder="Note", help="Bitte hier die Note eintragen!", step=1, min_value=1, max_value=5)
            grade_input = st.session_state.key_grade_input
        else:
            #st.session_state.key_K_input == False:
            grade_input = "K"
        
        
        
        #if no comment is present, set comment_result to None
        if comment_result==[]:
            comment_result = ""
        else:
            comment_result = comment_result[0][0]
        #input for comment
        st.text_area(label="Kommentar", placeholder="Kommentar", help="Bitte hier ihren Kommentar eingeben", key="key_comment_input",value=comment_result)
        

        #if no weight is present, set weight_result to 0.0
        if weight_result==[]:
            weight_result = 100
        else:
            weight_result = weight_result[0][0]
        #input for weight
            
    
        if st.session_state.key_K_input == True:
            st.write(F"Das Kind war krank: Die Aufgabe fließt nicht in die Benotung.")
            weight_input = 999

        else:
            if weight_result == 999:
                weight_result = 100
            st.slider(label="Gewichtung/Maximale Punkte", key="key_weight_input", value=weight_result, min_value=50, max_value=150, step=50, help="Bitte hier die Gewichtung eintragen! [**Leicht:** 50, **Normal:** 100, **Schwer:** 150] Diese entspricht der maximal erreichbaren Punkteanzahl.")
            st.write(F"Das Kind bekommt **{gradeTOPercentage(st.session_state.key_grade_input)/100*st.session_state.key_weight_input}** Punkte gutgeschrieben.")
            weight_input = st.session_state.key_weight_input

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
            db.update_or_save_grade(kid_id, book_id, assignment_ID, grade_input, st.session_state.key_comment_input, weight_input, st.session_state.key_date_input, st.session_state.key_assignment_description_input)
            #seite neu laden
            st.experimental_rerun()
            

        if button_col2.button("Löschen", help="Klicken Sie hier um die Note zu löschen!"):
            db.delete_grade(kid_id, book_id, assignment_ID)
            #seite neu laden
            st.experimental_rerun()

        db.__del__()



#----------------------------SESSIONSTATES------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()

elif st.session_state.showSession == 2:
    detailansicht()

else:
    pass
