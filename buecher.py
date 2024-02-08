from st_pages import Page, show_pages, add_page_title
import streamlit as st
import time

# Initialize session state
if "buchanlegen" not in st.session_state:
    st.session_state.buchanlegen = True

add_page_title()

cl1, cl2 = st.columns([0.15,0.85])
button1_ph = cl1.button("Anlegen", on_click=lambda: st.session_state.__setitem__("buchanlegen", True), help="Klicken Sie hier um ein neues Buch anzulegen!")
button2_ph = cl2.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("buchanlegen", False), help="Klicken Sie hier um ein Buch zu bearbeiten!")

container = st.container()

def button_anlegen_clicked():
    name = st.session_state.key_name
    seitenanzahl = st.session_state.key_seitenanzahl
    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Das Buch '{name}' mit {seitenanzahl} Seite(n) wurde erfolgreich gespeichert!")
        st.session_state.key_name = ""
        st.session_state.key_seitenanzahl = 0

def button_speichern_clicked():
    namealt = st.session_state.key_ausg_buch
    name = st.session_state.key_name_neu
    seitenanzahl = st.session_state.key_seitenanzahl_neu
    #überprüfen ob es diesen Buchnamen noch nicht in der Datenbank gibt
    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Das Buch '{namealt}' wurde in '{name}' mit {seitenanzahl} Seiten geändert!")

    

def button_loeschen_clicked():
    name = st.session_state.key_ausg_buch
    #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
    if name == "":
        st.error("Bitte wählen Sie ein Buch aus!")
    else:
        with st.spinner("Buch wird gelöscht..."):
            # Daten wirklich löschen
            pass
        st.success(F"Das Buch '{name}' wurde erfolgreich gelöscht!")


def anlegen():
     
    container.text_input(label="Name", key="key_name", placeholder="Name des Buches", help="Bitte hier Namen des Buches eingeben das Sie anlegen wollen!")
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl", placeholder="Seitenanzahl", help="Bitte hier die Seitenanzahl des Buches eingeben das Sie anlegen wollen!", step=1, min_value=0)

    container.button(label="Speichern", on_click=button_anlegen_clicked, help="Klicken Sie hier um das Buch zu speichern!")

        
def bearbeiten():
    buecher = ["Buch 1", "Buch 2", "Buch 3"]    #tatstächlich aus der Datenbank holen

    container.selectbox(label="Buch auswählen",key="key_ausg_buch", index=0, options=buecher, help="Bitte hier das Buch auswählen das Sie bearbeiten wollen!")
    container.text_input(label="Name", key="key_name_neu", placeholder="neuer Name des Buches", value=st.session_state.key_ausg_buch, help="Bitte hier den neuen Namen des Buches eingeben!")
    #value aus der datenbank holen: Seitenanzahl des ausgewählten Buches
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl_neu", placeholder="neue Seitenanzahl", help="Bitte hier die neue Seitenanzahl des Buches eingeben!", step=1, min_value=0)

    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Buch zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.buchanlegen:
    anlegen()
else:
    bearbeiten()

