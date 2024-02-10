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
            

            df = pd.DataFrame(columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])
            df.insert(0, 'Kid Name', kids)  # Insert Kid Names as the first column


            for i in range(1, seitenanz_aus_DB + 1):
                df.insert(i+2, f"S. {i} Link", [f"https://www.google.com/search?q={kid}" for kid in kids])

            

                st.data_editor(
                    data=df,
                    column_config={
                            f"S. {i} Link": st.column_config.LinkColumn(
                           f"S. {i}",
                            help="Link to the page",
                            display_text="Link",
                            )
                    }
                )

            
            ''''
            st.data_editor(
                data=df,
                column_config={

                    f"S. {i}": st.column_config.SelectboxColumn(
                        f"S. {i}",
                        help="Selectbox for grade",
                        width="small",
                        options=["Klicken"],
                        required=True,
                    ) for i in range(1, seitenanz_aus_DB + 1)
                },
                hide_index=True,
            )'''



            if st.button("Speichern"):
                #iteriere durch den data editor und speichere die Daten in die Datenbank
                for row in df.itertuples():
                    all_data = df.iloc[row]
                    st.success(f"{all_data} wurde erfolgreich gespeichert!")
                    #st.success(f"funkt")
                     


        # Open file explorer for user to choose file path
        file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

        # Export the DataFrame to the specified file path
        if st.button("Export to CSV"):
            df.to_csv(file_path, sep='\t')
            st.success(f"Data successfully exported to {file_path}")




        #container.button(label="Exportieren", on_click=lambda: st.session_state.__setitem__("showSession", 2), # button_export_clicked, Wechsel zu showSession 2
                         # help="Klicken Sie hier um diese Übersicht zu exportieren!")
    else:
        container.write("Das Buch hat keine Seitenanzahl.")



def update_db_from_data_editor(df):
    db = DB()
    for row in df.itertuples():
        index = df.index.get_loc(row.Index)
        kid_name = df.iloc[row, 1]
        #get all grades for the kid
        grades = df.iloc[row, 2:]

        db.query("INSERT INTO Kid (firstname, lastname) VALUES (?, ?)", (kid_name.split()[0], kid_name.split()[1]))

        kid_id = db.query("SELECT id FROM Kid WHERE firstname = ? AND lastname = ?", (kid_name.split()[0], kid_name.split()[1]))[0][0]
        #db.query("INSERT INTO Page (kid_id, book_id, page_number, grade) VALUES (?, ?, ?, ?)", (kid_id, 1, i + 1, page))

        for i, grade in enumerate(grades):
            db.query("INSERT INTO Page (kid_id, book_id, page_number, grade) VALUES (?, ?, ?, ?)", (kid_id, 1, i + 1, grades[i]))







#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()

#elif st.session_state.showSession == 2:
    #update_db_from_data_editor()
else:
    pass
