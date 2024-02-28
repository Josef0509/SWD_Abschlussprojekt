import streamlit as st
import st_pages as stp
from db import DB
from encode import hash
import logging
# Function to show the main content

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s %(message)s')

st.set_page_config(layout="wide", page_title="VSGrade", page_icon=":school:")

def main():
    st.markdown("""
        # Willkommen zu VSGrade :school: 

        ---
                
        Beginnen Sie mit der Navigation auf der linken Seite.
                
        ---
    	"""
    )

    st.header("Dokumentation")
    st.markdown("""
                Dort können Sie jederzeit die Dokumentation zu diesem Programm einsehen.
                #
                #
                #
                #
                """
                )
    st.markdown("powered by ObSt")
    

    pages = [
        stp.Page("doc.py", "Dokumentation", ":page_with_curl:"),
        stp.Page("buecher.py", "Bücher", ":books:"),
        stp.Page("schueler.py", "Schüler", ":student:"),
        stp.Page("gruppen.py", "Gruppen", ":man-woman-girl-girl:"),
        stp.Page("benotung.py", "Benotung", ":1234:"),
        stp.Page("einstellungen.py", "Einstellungen", ":gear:")
    ]
        
    stp.show_pages(pages)
    

def login_pressed(name:str, password:str, token:str):
    # Load the credentials from the database
    db = DB()
    db_usernames, db_passwords = db.get_credentials()
    
    # Get the hexadecimal representation of the hashed password
    hashed_password = hash(password)
    hashed_token = None
    if token != None:
        hashed_token = hash(token)    

    token_is_valid_now = False
    token_was_valid_before = False

    if db.get_session_token() is None or db.get_session_token() == "":
        if db.check_token(hashed_token):
            token_is_valid_now = True           
    else:
        token_was_valid_before = True            
    

    if name in db_usernames and hashed_password == db_passwords[db_usernames.index(name)]:

        if token_is_valid_now or token_was_valid_before: 
            st.session_state.logged_in = True
            db.set_UserToken_inSession(name, hashed_token)
            db.__del__()
            logging.info(f"User {name} logged in.")
        
    else:
        st.error("The credentials you entered are incorrect.")

def login():
    st.title("Login Page")
    # Insert a form
    #ABGABE: Username und  PW für Julian und Matthias anzeigen
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")

    db = DB()

    if db.get_session_token() is None or db.get_session_token() == "":
        token = st.text_input("Token")

        st.button("Programm aktivieren", on_click=lambda: login_pressed(name, password, token))
    else:
        st.button("Login", on_click=lambda: login_pressed(name, password, None))
    db.__del__()
    
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()
