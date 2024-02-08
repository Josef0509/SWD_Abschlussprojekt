from st_pages import Page, show_pages, add_page_title
import streamlit as st
import pandas as pd
import numpy as np
import time

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1

add_page_title()

cl1, cl2, cl3 = st.columns([0.2,0.2,0.6])
button1_ph = cl1.button("Teilnehmer", on_click=lambda: st.session_state.__setitem__("showSession", 1), help="Klicken Sie hier um Kinder in Gruppen einzuteilen!")
button2_ph = cl2.button("Anlegen", on_click=lambda: st.session_state.__setitem__("showSession", 2), help="Klicken Sie hier um eine neue Gruppe anzulegen!")
button3_ph = cl3.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("showSession", 3), help="Klicken Sie hier um eine bestehende Gruppe zu bearbeiten!")

container = st.container()

def button_export_clicked():
    with st.spinner("Daten werden exportiert..."):
            # Daten wirklich exportieren
            pass
    st.success(F"Erfolgsmeldung")

def button_gruppe_speichern_clicked():
    name = st.session_state.key_gruppen_name
    if name == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Gruppe wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Die Gruppe '{name}' wurde erfolgreich gespeichert!")
        st.session_state.key_gruppen_name = ""
    
def button_loeschen_clicked():
    name = st.session_state.key_ausg_Gruppe
    if name == "":
        st.error("Bitte wählen Sie eine Gruppe aus!")
    else:

        with st.spinner("Gruppe wird gelöscht..."):
            # Daten wirklich löschen
            pass
        st.success(F"Die Gruppe '{name}' wurde erfolgreich gelöscht!")

def button_speichern_clicked():
    pass

def button_speichern_clicked_bearbeiten():
    pass

def teilnehmer():
    gruppen = ["G1", "G2", "G3"]    #tatstächlich aus der Datenbank holen
    container.selectbox(label="Gruppe auswählen",key="key_ausg_Gruppe", index=0, options=gruppen, help="Bitte hier die Gruppe auswählen die Sie anzeigen wollen!")
    container.checkbox("Schüler 1")
    container.checkbox("Schüler 2")
    container.checkbox("Schüler 3")
    #loop durch alle Schüler und erstellen einer checkbox
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")

def anlegen():
    container.text_input(label="Gruppenname", key="key_gruppen_name", placeholder="Name der Gruppe", help="Bitte hier den Namen der Gruppen eingeben die Sie anlegen wollen!")
    container.button(label="Speichern", on_click=button_gruppe_speichern_clicked, help="Klicken Sie hier um das Kind zu speichern!")

def bearbeiten():
    gruppen = ["G1", "G2", "G3"]     #tatstächlich aus der Datenbank holen

    container.selectbox(label="Gruppe auswählen",key="key_ausg_Gruppe", index=0, options=gruppen, help="Bitte hier die Gruppe auswählen die Sie bearbeiten wollen!")
    container.text_input(label="Gruppenname", key="key_name_gruppe_neu",value=st.session_state.key_ausg_Gruppe, placeholder="Name der Gruppe", help="Bitte hier den neuen Namen der Gruppe eingeben!")
    
    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um die Gruppe zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked_bearbeiten, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.showSession == 1:
    teilnehmer()
elif st.session_state.showSession == 2:
    anlegen()
else:
    bearbeiten()

