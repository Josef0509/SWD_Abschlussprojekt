from st_pages import Page, show_pages, add_page_title
import streamlit as st
from db import DB
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
    #initialize database
    db = DB()
    name = st.session_state.key_name
    seitenanzahl = st.session_state.key_seitenanzahl
    autonumbering = st.session_state.key_autonumerierung
    
    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    elif db.query("SELECT name FROM Book WHERE name = ?", (name,)) != []:
        st.error("Dieses Buch existiert bereits! Sie können es bearbeiten!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            db.query("INSERT INTO Book (name, pages, autonumbering) VALUES (?, ?, ?)", (name, seitenanzahl, autonumbering))
        st.success(F"Das Buch '{name}' mit {seitenanzahl} Seite(n) wurde erfolgreich gespeichert!")
        st.session_state.key_name = ""
        st.session_state.key_seitenanzahl = 0

    db.__del__() 


def button_speichern_clicked():
    namealt = st.session_state.key_ausg_buch
    name = st.session_state.key_name_neu
    seitenanzahl = st.session_state.key_seitenanzahl_neu
    autonumbering_neu = st.session_state.key_autonumerierung_neu
    #überprüfen ob es diesen Buchnamen noch nicht in der Datenbank gibt
    db = DB()

    if namealt == None or name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            if name == namealt or not bool(db.query("SELECT 1 FROM Book WHERE name = ?", (name,))):
                #update that book
                db.query("UPDATE Book SET name = ?, pages = ?, autonumbering = ? WHERE name = ?", (name, seitenanzahl, autonumbering_neu, namealt))
                st.success(F"Das Buch '{namealt}' wurde in '{name}' mit {seitenanzahl} Seiten geändert!")
            else:
                st.error("Es gibt bereits ein Buch mit diesem Namen!")

def button_loeschen_clicked():
    db = DB()
    name = st.session_state.key_ausg_buch
    #überprüfen ob es noch keine Eintragungen zu diesem Buchnamen gibt
    if name == "":
        st.error("Bitte wählen Sie ein Buch aus!")
    else:
        with st.spinner("Buch wird gelöscht..."):
            db.query("DELETE FROM Book WHERE name = ?", (name,))
        st.success(F"Das Buch '{name}' wurde erfolgreich gelöscht!")


def anlegen():
    container.text_input(label="Name", key="key_name", placeholder="Name des Buches", help="Bitte hier Namen des Buches eingeben das Sie anlegen wollen!")
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl", placeholder="Seitenanzahl", help="Bitte hier die Seitenanzahl des Buches eingeben das Sie anlegen wollen!", step=1, min_value=0)
    container.toggle("Autonumerierung", key="key_autonumerierung", value=True, help="Klicken Sie hier um die Spalten bei der Benotung automatisch zu nummerieren!")
    container.button(label="Speichern", on_click=button_anlegen_clicked, help="Klicken Sie hier um das Buch zu speichern!")

        
def bearbeiten():
    #initialize database
    db = DB()
    buecher = db.query("SELECT name FROM Book")     #returns tuples
    buecher = [buch[0] for buch in buecher]   #convert to list
    container.selectbox(label="Buch auswählen",key="key_ausg_buch", index=0, options=buecher, help="Bitte hier das Buch auswählen das Sie bearbeiten wollen!")
    container.text_input(label="Name", key="key_name_neu", placeholder="neuer Name des Buches", value=st.session_state.key_ausg_buch, help="Bitte hier den neuen Namen des Buches eingeben!")

    seitenanz_aus_DB = db.query("SELECT pages FROM Book WHERE name = ?", (st.session_state.key_ausg_buch,))
    if seitenanz_aus_DB == []:
        seitenanz_aus_DB = 0
    else:
        seitenanz_aus_DB = seitenanz_aus_DB[0][0]
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl_neu", value=seitenanz_aus_DB, placeholder="neue Seitenanzahl", help="Bitte hier die neue Seitenanzahl des Buches eingeben!", step=1, min_value=0)
    
    autonum_aus_DB = db.query("SELECT autonumbering FROM Book WHERE name = ?", (st.session_state.key_ausg_buch,))
    if autonum_aus_DB == []:
        autonum_aus_DB = False
    else:
        autonum_aus_DB = autonum_aus_DB[0][0]
    container.toggle("Autonumerierung", key="key_autonumerierung_neu", value=autonum_aus_DB, help="Klicken Sie hier um die Spalten bei der Benotung automatisch zu nummerieren!")

    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Buch zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")

    db.__del__()


if st.session_state.buchanlegen:
    anlegen()
else:
    bearbeiten()

