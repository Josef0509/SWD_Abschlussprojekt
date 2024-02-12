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
button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1),
                         help="Klicken Sie hier um zur Übersicht zu gelangen!")
button2_ph = cl2.button("Detailansicht", on_click=lambda: st.session_state.__setitem__("showSession", 2),
                        help="Klicken Sie hier um die Detailansicht zu sehen!")


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
def detailansicht(selected_kid, selected_book, selected_page):
    db = DB()
    
    print(selected_book)
    print(selected_kid)
    print(selected_page)

    #get the info for the selected kid and page
    
    #selected _page aus liste entfernen
    selected_page = selected_page[0]
    
    for kid_name in selected_kid:
        kid_id_result = db.query("SELECT kidID FROM Kid WHERE firstname = ?", (kid_name,))
        
        if kid_id_result:
            kid_id = kid_id_result[0][0]
            st.write("kid_id")
            st.header(kid_id)
            

            book_id_result = db.query("SELECT bookID FROM Book WHERE name = ?", (selected_book,))
            
            if book_id_result:
                book_id = book_id_result[0][0]
                st.write("Book_id")
                st.header(book_id)

                grade_result = db.query("SELECT grade FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id,selected_page))
                print(grade_result)
                st.write("Grade")
                st.header(grade_result)

                comment_result = db.query("SELECT comment FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                print(comment_result)
                st.write("Comment")
                st.header(comment_result)



                weight_result = db.query("SELECT weight FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                print(weight_result)
                st.write("Weight")
                st.header(weight_result)


                date_result = db.query("SELECT date FROM Grade WHERE kidID = ? AND bookID = ? AND page = ?", (kid_id, book_id, selected_page))
                print(date_result)
                st.write("Date")
                st.header(date_result)



            else:
                st.warning(f"No book found for {selected_book}")
        else:
            st.warning(f"No kid found for {kid_name}")
        

        







        





#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()

elif st.session_state.showSession == 2:
    selected_kid, selected_book, selected_page, seitenanz_aus_DB = uebersicht()
    detailansicht(selected_kid, selected_book, selected_page)

else:
    pass
