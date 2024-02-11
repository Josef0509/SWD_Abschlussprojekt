from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB
from tkinter import filedialog

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()

cl1, cl2, cl3 = st.columns([0.15, 0.15, 0.7])


container = st.container()





# ------------------------------------------------------------------------------------------------------------------------------
def uebersicht():
    st.header("Benotungsübersicht")
    db = DB()

    buecher = db.query("SELECT name FROM Book")  # returns tuples
    buecher = [buch[0] for buch in buecher] if buecher else []

    selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")

    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None

    

    kids = db.query("SELECT firstname, lastname FROM Kid")     #returns tuples
    if kids != []:
        kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list


    if seitenanz_aus_DB:
        container.write(f"Seitenanzahl: {seitenanz_aus_DB}")



        # Fetch kid names and create a DataFrame with random data
        kids = db.query("SELECT firstname, lastname FROM Kid")

        if kids != []:

            kids = [f"{kid[0]} {kid[1]}" for kid in kids]
            
            #Make DataFrame for table
            df = pd.DataFrame(columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])
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

            

            #transponiere die Auswahl und füge die Spalte "Select" hinzu
            selection = selection.transpose()
            selection.insert(0, "Select", False)
            selection.insert(0, "Seite", selection.index)

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


            print(selected_page)
            st.write(selected_page)
            


            
        

        if st.button("Detailansicht"):
            #print(selection)
            st.write("Your selection:")
            st.write(selection)

            #lade die daten für die detailansicht, dazu kind, buch und seite info aus der datenbank
            #und zeige die detailansicht



            print(selected_kid)
            print(selected_page)

            #get the info for the selected kid and page
            
            kid_ids = []
            for kid_name in selected_kid:
                kid_id = db.query("SELECT kidID FROM Kid WHERE firstname = ?", (kid_name,))
                st.write("kid_id")
                st.header(kid_id)
                

                for book in selected_book:
                    book_id = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
                    st.write("Book_id")
                    st.header(book_id)

                    for page in selected_page:
                        grade = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, page))[0][0]
                        st.write("Grade")
                        st.header(grade)

                        comment = db.query("SELECT comment FROM Page WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, page))[0][0]
                        st.write("Comment")
                        st.header(comment)

                        weight = db.query("SELECT weight FROM Page WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, page))[0][0]
                        st.write("weight")
                        st.header(weight)

                        date = db.query("SELECT date FROM Page WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, page))[0][0]
                        st.write("date")
                        st.header(date)
            

            













        # Open file explorer for user to choose file path
        file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

        # Export the DataFrame to the specified file path
        if st.button("Export to CSV"):
            df.to_csv(file_path, sep='\t')
            st.success(f"Data successfully exported to {file_path}")


    else:
        container.write("Das Buch hat keine Seitenanzahl.")





#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()


else:
    pass
