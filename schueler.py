from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
import time

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()

cl1, cl2, cl3 = st.columns([0.15,0.15,0.7])
button1_ph = cl1.button("Übersicht", on_click=lambda: st.session_state.__setitem__("showSession", 1), help="Klicken Sie hier um zur individuellen Schüleransicht zu gelangen!")
button2_ph = cl2.button("Anlegen", on_click=lambda: st.session_state.__setitem__("showSession", 2), help="Klicken Sie hier um ein neues Kind anzulegen!")
button3_ph = cl3.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("showSession", 3), help="Klicken Sie hier um ein bestehendes Kind zu bearbeiten!")

container = st.container()

def button_export_clicked():
    with st.spinner("Daten werden exportiert..."):
            # Daten wirklich exportieren
            pass
    st.success(F"Erfolgsmeldung")

def button_kind_speichern_clicked():
    vorname = st.session_state.key_vorname_schueler
    nachname = st.session_state.key_nachname_schueler
    if vorname == "" or nachname == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Kind wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Das Kind '{vorname}' '{nachname}' wurde erfolgreich gespeichert!")
        st.session_state.key_vorname_schueler = ""
        st.session_state.key_nachname_schueler = ""
    
def button_loeschen_clicked():
    name = st.session_state.key_ausg_Kind
    if name == "":
        st.error("Bitte wählen Sie ein Kind aus!")
    else:

        with st.spinner("Kind wird gelöscht..."):
            # Daten wirklich löschen
            pass
        st.success(F"Das Kind '{name}' wurde erfolgreich gelöscht!")

def button_speichern_clicked():
    pass

def uebersicht():
    kinder = ["Schüler 1", "Schüler 2", "Schüler 3"]    #tatstächlich aus der Datenbank holen
    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kinder, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Fach1", "Fach2", "Fach3"])
    container.line_chart(chart_data)
    container.write("Aktuelle Noten:")
    #notenstand ermitteln
    container.write("Fach 1: 1.45")
    container.write("Fach 2: 2.01")
    container.write("Fach 3: 3.23")
    container.button(label="Exportieren", on_click=button_export_clicked, help="Klicken Sie hier um diese Übersicht zu exportieren!")

def anlegen():
    container.text_input(label="Vorname", key="key_vorname_schueler", placeholder="Vorname des Kindes", help="Bitte hier den Vornamen des Kindes eingeben das Sie anlegen wollen!")
    container.text_input(label="Nachname", key="key_nachname_schueler", placeholder="Nachname des Kindes", help="Bitte hier den Nachnamen des Kindes eingeben das Sie anlegen wollen!")

    container.button(label="Speichern", on_click=button_kind_speichern_clicked, help="Klicken Sie hier um das Kind zu speichern!")

def bearbeiten():
    kinder = ["Schüler 1", "Schüler 2", "Schüler 3"]    #tatstächlich aus der Datenbank holen

    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kinder, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    container.text_input(label="Vorname", key="key_vorname_schueler_neu", placeholder="Vorname des Kindes", help="Bitte hier den neuen Vornamen des Kindes eingeben!")
    container.text_input(label="Nachname", key="key_nachname_schueler_neu", placeholder="Nachname des Kindes", help="Bitte hier den neuen Nachnamen des Kindes eingeben!")

    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Kind zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.showSession == 1:
    uebersicht()
elif st.session_state.showSession == 2:
    anlegen()
else:
    bearbeiten()

