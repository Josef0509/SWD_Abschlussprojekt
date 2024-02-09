from st_pages import Page, show_pages, add_page_title
import streamlit as st

import pandas as pd
import numpy as np
import time
from db import DB

# Initialize session state
if "showSession" not in st.session_state:
    st.session_state.showSession = 1
=======
import time



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
    db = DB()
    vorname = st.session_state.key_vorname_schueler
    nachname = st.session_state.key_nachname_schueler
    if vorname == "" or nachname == "":
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        if not bool(db.query("SELECT 1 FROM Kid WHERE firstname = ? AND lastname = ?", (vorname,nachname))):
            with st.spinner("Kind wird gespeichert..."):
                db.query("INSERT INTO Kid (firstname, lastname, groupID) VALUES (?, ?, ?)", (vorname, nachname, 1)) #groupID TBD

            st.success(F"Das Kind '{vorname} {nachname}' wurde erfolgreich gespeichert!")
            st.session_state.key_vorname_schueler = ""
            st.session_state.key_nachname_schueler = ""
        else:
            st.error("Dieses Kind existiert bereits!")
    
def button_loeschen_clicked():
    db = DB()
    name = st.session_state.key_ausg_Kind
    vorname = name.split(" ")[0]
    nachname = name.split(" ")[1]

    if name == None:
        st.error("Bitte wählen Sie ein Kind aus!")
    else:
        with st.spinner("Kind wird gelöscht..."):
            db.query("DELETE FROM Kid WHERE firstname = ? AND lastname = ?", (vorname, nachname))
        st.success(F"Das Kind '{name}' wurde erfolgreich gelöscht!")

def button_speichern_clicked():
    name_alt = st.session_state.key_ausg_Kind
    if name_alt != None:
        vorname_alt = name_alt.split(" ")[0]
        nachname_alt = name_alt.split(" ")[1]

        vorname_neu = st.session_state.key_vorname_schueler_neu
        nachname_neu = st.session_state.key_nachname_schueler_neu

        if vorname_neu == "" or nachname_neu == "":
            st.error("Bitte füllen Sie alle Felder aus!")
        else: 
            db = DB()
            if not bool(db.query("SELECT 1 FROM Kid WHERE firstname = ? AND lastname = ?", (vorname_neu,nachname_neu))):
                with st.spinner("Kind wird gespeichert..."):
                    db.query("UPDATE Kid SET firstname = ?, lastname = ? WHERE firstname = ? AND lastname = ?", (vorname_neu, nachname_neu, vorname_alt, nachname_alt))
                st.success(F"Das Kind '{vorname_alt} {nachname_alt}' wurde in '{vorname_neu} {nachname_neu}' geändert!")
            else:
                st.error("Dieses Kind existiert bereits!")
    else:
        st.error("Bitte wählen Sie ein Kind aus!")


def uebersicht():
    db = DB()
    kids = db.query("SELECT firstname, lastname FROM Kid")     #returns tuples
    if kids != []:
        kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list
    
    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kids, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    
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
    db = DB()
    kids = db.query("SELECT firstname, lastname FROM Kid")     #returns tuples
    if kids != []:
        kids = [kid[0]+" "+kid[1] for kid in kids]   #convert to list

    container.selectbox(label="Kind auswählen",key="key_ausg_Kind", index=0, options=kids, help="Bitte hier das Kind auswählen das Sie anzeigen wollen!")
    
    if kids != []:
        vorname_alt = st.session_state.key_ausg_Kind.split(" ")[0]
        nachname_alt = st.session_state.key_ausg_Kind.split(" ")[1]
    else:
        vorname_alt = ""
        nachname_alt = ""
    
    container.text_input(label="Vorname", key="key_vorname_schueler_neu",value=vorname_alt, placeholder="Vorname des Kindes", help="Bitte hier den neuen Vornamen des Kindes eingeben!")
    container.text_input(label="Nachname", key="key_nachname_schueler_neu", value=nachname_alt, placeholder="Nachname des Kindes", help="Bitte hier den neuen Nachnamen des Kindes eingeben!")

    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Kind zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")


if st.session_state.showSession == 1:
    uebersicht()
elif st.session_state.showSession == 2:
    anlegen()
else:
    bearbeiten()

def button_export_clicked():
    person = st.session_state.key_ausg_person
    if person == "":
        st.error("Bitte wählen Sie eine Person aus!")
    else:
        with st.spinner("Person wird exportiert..."):
            pass
        st.success(F"Die Person '{person}' wurde erfolgreich exportiert!")





tab_uebersicht, tab_bearbeiten = st.tabs(["Übersicht", "Bearbeiten"])

with tab_uebersicht:
    personen = ["Josef", "Giuseppe 2", "Josi"]    #tatstächlich aus der Datenbank holen

    st.selectbox(label="Person auswählen",key="key_ausg_person", index=0, options=personen, help="Bitte hier die Person auswählen die Sie anzeigen wollen!")
    

    st.button(label="Export", on_click=button_export_clicked, help="Klicken Sie hier um die Person zu exportieren!")
