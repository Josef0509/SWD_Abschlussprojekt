from st_pages import Page, show_pages, add_page_title
import streamlit as st
import time


add_page_title()

def button_anlegen_clicked():
    name = st.session_state.key_name
    seitenanzahl = st.session_state.key_seitenanzahl
    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Das Buch '{name}' mit {seitenanzahl} Seiten wurde erfolgreich gespeichert!")
        st.session_state.key_name = ""
        st.session_state.key_seitenanzahl = 0

def button_speichern_clicked():
    name = st.session_state.key_name_neu
    seitenanzahl = st.session_state.key_seitenanzahl_neu
    #überprüfen ob es diesen Buchnamen noch nicht in der Datenbank gibt
    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            pass
        st.success(F"Das Buch '{name}' mit {seitenanzahl} Seiten wurde erfolgreich geändert!")

    

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


tab_anlegen, tab_bearbeiten = st.tabs(["Anlegen", "Bearbeiten"])

with tab_anlegen:
    
    st.text_input(label="Name", key="key_name", placeholder="Name des Buches", help="Bitte hier Namen des Buches eingeben das Sie anlegen wollen!")
    st.number_input(label="Seitenanzahl", key="key_seitenanzahl", placeholder="Seitenanzahl", help="Bitte hier die Seitenanzahl des Buches eingeben das Sie anlegen wollen!", step=1, min_value=0)

    st.button(label="Speichern", on_click=button_anlegen_clicked, help="Klicken Sie hier um das Buch zu speichern!")

        
with tab_bearbeiten:
    buecher = ["Buch 1", "Buch 2", "Buch 3"]    #tatstächlich aus der Datenbank holen

    st.selectbox(label="Buch auswählen",key="key_ausg_buch", index=0, options=buecher, help="Bitte hier das Buch auswählen das Sie bearbeiten wollen!")
    st.text_input(label="Name", key="key_name_neu", placeholder="neuer Name des Buches", value=st.session_state.key_ausg_buch, help="Bitte hier den neuen Namen des Buches eingeben!")
    #value aus der datenbank holen: Seitenanzahl des ausgewählten Buches
    st.number_input(label="Seitenanzahl", key="key_seitenanzahl_neu", placeholder="neue Seitenanzahl", help="Bitte hier die neue Seitenanzahl des Buches eingeben!", step=1, min_value=0)

    st.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Buch zu löschen!")
    st.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")
