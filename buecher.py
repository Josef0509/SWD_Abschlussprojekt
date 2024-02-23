from st_pages import Page, show_pages, add_page_title
import streamlit as st
from db import DB
from c_buecher import Book

st.set_page_config(layout="wide", page_title="Bücher", page_icon=":books:")
st.title(":books:"+" Bücher")

#Initialize session state
if "buchanlegen" not in st.session_state:
    st.session_state.buchanlegen = True

#set up page layout
cl1, cl2 = st.columns([0.15,0.85])
button1_ph = cl1.button("Anlegen", on_click=lambda: st.session_state.__setitem__("buchanlegen", True), help="Klicken Sie hier um ein neues Buch anzulegen!")
button2_ph = cl2.button("Bearbeiten", on_click=lambda: st.session_state.__setitem__("buchanlegen", False), help="Klicken Sie hier um ein Buch zu bearbeiten!")

container = st.container()
#end page layout

def button_anlegen_clicked():
    name = st.session_state.key_name
    seitenanzahl = st.session_state.key_seitenanzahl
    autonumbering = st.session_state.key_autonumerierung
    
    new_book = Book(name, seitenanzahl, autonumbering)

    if name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    elif new_book.check_if_book_name_exists():
        st.error("Dieses Buch existiert bereits! Sie können es bearbeiten!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            # Daten wirklich speichern
            new_book.save_new_book()

        st.success(F"Das Buch '{name}' mit {seitenanzahl} Seite(n) wurde erfolgreich gespeichert!")
        st.session_state.key_name = ""
        st.session_state.key_seitenanzahl = 0


def button_speichern_clicked():
    namealt = st.session_state.key_ausg_buch
    name = st.session_state.key_name_neu
    seitenanzahl = st.session_state.key_seitenanzahl_neu
    autonumbering_neu = st.session_state.key_autonumerierung_neu
    update_book = Book(name, seitenanzahl, autonumbering_neu)

    if namealt == None or name == "" or seitenanzahl <= 0:
        st.error("Bitte füllen Sie alle Felder aus!")
    elif update_book.check_if_book_name_exists():
        st.error("Es gibt bereits ein Buch mit diesem Namen!")
    else:
        with st.spinner("Buch wird gespeichert..."):
            update_book.update(namealt)
        
        st.success(F"Das Buch '{namealt}' wurde in '{name}' mit {seitenanzahl} Seiten geändert!")


def button_loeschen_clicked():
    name = st.session_state.key_ausg_buch
    delete_book = Book(name, 0, False)
    if name == "":
        st.error("Bitte wählen Sie ein Buch aus!")
    else:
        with st.spinner("Buch wird gelöscht..."):
            delete_book.delete()
        st.success(F"Das Buch '{name}' wurde erfolgreich gelöscht!")


def anlegen():
    container.text_input(label="Name", key="key_name", placeholder="Name des Buches", help="Bitte hier Namen des Buches eingeben das Sie anlegen wollen!")
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl", placeholder="Seitenanzahl", help="Bitte hier die Seitenanzahl des Buches eingeben das Sie anlegen wollen!", step=1, min_value=0)
    container.toggle("Autonumerierung", key="key_autonumerierung", value=True, help="Klicken Sie hier um die nächste Seite bei der Benotung automatisch vorauszuwählen!")
    container.button(label="Speichern", on_click=button_anlegen_clicked, help="Klicken Sie hier um das Buch zu speichern!")

        
def bearbeiten():
    #initialize database
    db = DB()   

    #load all book names from the database
    buecher = db.load_books()   
    
    #fill the selectbox with the book names and copy name to text_input
    container.selectbox(label="Buch auswählen",key="key_ausg_buch", index=0, options=buecher, help="Bitte hier das Buch auswählen das Sie bearbeiten wollen!")
    container.text_input(label="Name", key="key_name_neu", placeholder="neuer Name des Buches", value=st.session_state.key_ausg_buch, help="Bitte hier den neuen Namen des Buches eingeben!")

    #load the book data from the selected book
    book_data = db.load_book_data(st.session_state.key_ausg_buch)
    seitenanz_aus_DB = book_data[0][2]
    autonum_aus_DB = book_data[0][3]

    #fill the inputs with data from the database
    container.number_input(label="Seitenanzahl", key="key_seitenanzahl_neu", value=seitenanz_aus_DB, placeholder="neue Seitenanzahl", help="Bitte hier die neue Seitenanzahl des Buches eingeben!", step=1, min_value=0)
    container.toggle("Autonumerierung", key="key_autonumerierung_neu", value=autonum_aus_DB, help="Klicken Sie hier um die Spalten bei der Benotung automatisch zu nummerieren!")

    #add buttons
    container.button(label="Löschen", on_click=button_loeschen_clicked, help="Klicken Sie hier um das Buch zu löschen!")
    container.button(label="Speichern", on_click=button_speichern_clicked, help="Klicken Sie hier um die Änderungen zu speichern!")

    #close database
    db.__del__()


#show the right page
if st.session_state.buchanlegen:
    anlegen()
else:
    bearbeiten()

