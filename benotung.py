from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
from db import DB

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()

cl1, cl2, cl3 = st.columns([0.15, 0.15, 0.7])

button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1), help="Klicken Sie hier um zur Benotungsübersicht zu gelangen!")

container = st.container()


def button_export_clicked():
    with st.spinner("Daten werden exportiert..."):
        # Daten wirklich exportieren
        pass
    st.success("Erfolgsmeldung")


def uebersicht():
    db = DB()

    buecher = db.query("SELECT name FROM Book")  # returns tuples
    if buecher != []:
        buecher = [buch[0] for buch in buecher]  # convert to list


    selected_book = container.selectbox(label="Buch auswählen", key="key_ausg_Buch", index=0, options=buecher, help="Bitte hier das Buch auswählen das Sie anzeigen wollen!")


    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (selected_book,))
    if seitenanz_aus_DB and seitenanz_aus_DB[0]:
        seitenanz_aus_DB = seitenanz_aus_DB[0][0]
        container.write(F"Seitenanzahl: {seitenanz_aus_DB}")
    else:
        container.write("Das Buch hat keine Seitenanzahl.")



    df = pd.DataFrame(np.random.randn(10, seitenanz_aus_DB), columns=[f"S. {i}" for i in range(1, seitenanz_aus_DB + 1)])

    st.table(df)




    container.write("Aktuelle Noten:")
    # notenstand ermitteln
    container.write("Fach 1: 1.45")
    container.write("Fach 2: 2.01")
    container.write("Fach 3: 3.23")

    container.button(label="Exportieren", on_click=button_export_clicked,
                     help="Klicken Sie hier um diese Übersicht zu exportieren!")




if st.session_state.showSession == 1:
    uebersicht()
else:
    pass
