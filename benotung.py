from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog
import datetime

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()

cl1, cl2, cl3 = st.columns([0.15, 0.15, 0.7])
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




# ------------------------------------------------------------------------------------------------------------------------------
def uebersicht():
    st.header("Benotungsübersicht")
    db = DB()

    selected_book = st.session_state.key_ausg_Buch
    
    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None

    book_id = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
    book_id = book_id[0][0]
        

    kids = db.query("SELECT firstname, lastname FROM Kid")     #returns tuples

    if kids != []: 
         kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list

    df = pd.DataFrame()

    if seitenanz_aus_DB:
        container.write(f"Seitenanzahl: {seitenanz_aus_DB}")

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

        


        # Create a copy of the DataFrame with an additional column for row-selections
        df_with_selections = df.copy()
        df_with_selections.insert(0, "Select", False)


        # Get dataframe row-selections from user with st.data_editor
        edited_df = st.data_editor(
            df_with_selections,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            disabled=df.columns,
        )

        # Get selected rows from the edited DataFrame
        selected_rows = edited_df[edited_df.Select]
        
        # Remove the selection column from the selected rows
        selection = selected_rows.drop('Select', axis=1)

        #extract the selected kids

        selected_kid = selection['Kid Name']
        selected_kid = [kid.split()[0] for kid in selected_kid]
        print(selected_kid)

        st.session_state.key_ausg_kid = selected_kid

        

        

        #transponiere die Auswahl und füge die Spalte "Select" hinzu
        selection = selection.transpose()
        selection.insert(0, "Select", False)
        selection.insert(1, "Seite", selection.index)

        #erstelle ein data editor für die ausgewählten Seiten
        edited_df_page = st.data_editor(
            selection,
            hide_index=True,
            column_config={"Select": st.column_config.CheckboxColumn(required=True)},
            width=1000,
            
        )

        # Get selected rows from the edited DataFrame
        selected_rows_page = edited_df_page[edited_df_page.Select]
        # Remove the selection column from the selected rows
        selection = selected_rows_page.drop('Select', axis=1)
        
        
        #extract the selected pages
        selected_page = selection['Seite']

        selected_page = [int(page.split()[1]) for page in selected_page]
        #konvertiere die seiten in int
        selected_page = [int(page) for page in selected_page]

        st.session_state.key_ausg_page = selected_page

        print(selected_page)
                    



            # Open file explorer for user to choose file path
        file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

        # Export the DataFrame to the specified file path
        if st.button("Export to CSV"):
            df.to_csv(file_path, sep='\t')
            st.success(f"Data successfully exported to {file_path}")


    else:
        container.write("Das Buch hat keine Seitenanzahl.")

    return selected_kid, selected_book, selected_page, seitenanz_aus_DB
            
    




#--------------------------------------------------------------------------------------------------------------------------------------
def detailansicht():


    db = DB()
    

    selected_book = st.session_state.key_ausg_Buch
    selected_kid = st.session_state.key_ausg_kid
    selected_page = st.session_state.key_ausg_page


    print(selected_book)
    print(selected_kid)
    

    #get the info for the selected kid and page
    
    #selected _page aus liste entfernen
    selected_page = selected_page[0]


    
    
    for kid_name in selected_kid:
        kid_id_result = db.query("SELECT kidID FROM Kid WHERE firstname = ?", (kid_name,))
        
        if kid_id_result:
            kid_id = kid_id_result[0][0]
            #st.write("kid_id")
            #st.header(kid_id)
            

            book_id_result = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
            
            if book_id_result:
                book_id = book_id_result[0][0]
                #st.write("Book_id")
                #st.header(book_id)

                grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id,selected_page))
                #print(grade_result)
                #st.write("Grade")
                #st.header(grade_result)

                comment_result = db.query("SELECT comment FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                #print(comment_result)
                #st.write("Comment")
                #st.header(comment_result)



                weight_result = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                #print(weight_result)
                #st.write("Weight")
                #st.header(weight_result)


                date_result = db.query("SELECT date FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                #print(date_result)
                #st.write("Date")
                #st.header(date_result)

                #if date_result == []:
                #    date_result = datetime.date.today()
                #else:
                #    date_result = date_result[0][0]

            else:
                st.warning(f"No book found for {selected_book}")
        else:
            st.warning(f"No kid found for {kid_name}")

        

        #INPUTS

        if grade_result==[]:
            grade_result = 1
        else:
            grade_result = grade_result[0][0]

        container.number_input(label = "Note", key="key_grade_input", value=grade_result, placeholder="Note", help="Bitte hier die Note eintragen!", step=1, min_value=1, max_value=5)
        
    
        
        if comment_result==[]:
            comment_result = None
        else:
            comment_result = comment_result[0][0]
        container.text_input(label="Kommentar", placeholder="Kommentar", help="Bitte hier ihren Kommentar eingeben", key="key_comment_input",value=comment_result)
        

        if weight_result==[]:
            weight_result = 0.0
        else:
            weight_result = weight_result[0][0]
        container.number_input(label = "Gewichtung", key="key_weight_input", value=weight_result, placeholder="Gewichtung", help="Bitte hier die Gewichtung eintragen!", step=1.0, min_value=0.0, max_value=100.0)
        


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
        container.date_input(label="Datum", help="Bitte hier das Datum eingeben", key="key_date_input", value=date_result)



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
