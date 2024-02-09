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
container = st.container()


cl1, cl2, cl3 = st.columns([0.15, 0.15, 0.7])








# ------------------------------------------------------------------------------------------------------------------------------
def button_export_clicked():
    db = DB()

    buecher = db.query("SELECT name FROM Book")  # returns tuples
    if buecher:
        buecher = [buch[0] for buch in buecher]  # convert to list

    selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")

    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None



    if seitenanz_aus_DB:
        #container.write(f"Seitenanzahl: {seitenanz_aus_DB}")
        #df = pd.DataFrame(np.random.randn(10, seitenanz_aus_DB), columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])

        
       # Open file explorer for user to choose file path
        file_path = "C:\\Users\\sandr\\OneDrive\\Desktop\\test\\export.csv"

        # Export the DataFrame to the specified file path
        if st.button("Export to CSV"):
            df.to_csv(file_path, sep='\t')
            st.success(f"Data successfully exported to {file_path}")

       # df.to_csv("export.csv", sep='\t')

        #st.success("Erfolgsmeldung: Daten wurden erfolgreich exportiert!")
        
    else:
        container.write("Das Buch hat keine Seitenanzahl.")
    
    button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1),
                        help="Klicken Sie hier um zur Benotungsübersicht zu gelangen!")


    







# ------------------------------------------------------------------------------------------------------------------------------
def uebersicht():
    db = DB()

    buecher = db.query("SELECT name FROM Book")  # returns tuples
    buecher = [buch[0] for buch in buecher] if buecher else []

    selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher,
                                        help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")

    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    seitenanz_aus_DB = seitenanz_aus_DB[0][0] if seitenanz_aus_DB and seitenanz_aus_DB[0] else None

    if seitenanz_aus_DB:
        container.write(f"Seitenanzahl: {seitenanz_aus_DB}")
        df = pd.DataFrame(np.random.randn(10, seitenanz_aus_DB), columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])
        st.table(df)

        container.write("Aktuelle Noten:")
        # notenstand ermitteln
        container.write("Fach 1: 1.45")
        container.write("Fach 2: 2.01")
        container.write("Fach 3: 3.23")

        container.button(label="Exportieren", on_click=lambda: st.session_state.__setitem__("showSession", 2), # button_export_clicked, Wechsel zu showSession 2
                          help="Klicken Sie hier um diese Übersicht zu exportieren!")
    else:
        container.write("Das Buch hat keine Seitenanzahl.")







#------------------------------------------------------------------------------------------------------------------------------
if st.session_state.showSession == 1:
    uebersicht()
elif st.session_state.showSession == 2:
    button_export_clicked()
else:
    pass
