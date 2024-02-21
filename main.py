import streamlit as st
import st_pages as stp
from db import DB
from encode import hash
# Function to show the main content

st.set_page_config(layout="centered", page_title="Notensoftware")

def main():
    st.title("Notensoftware")
    st.markdown(
        """
        Beginnen Sie mit der Navigation auf der linken Seite.
        """
    )
    pages = [
        stp.Page("doc.py", "Dokumentation", ":page_with_curl:"),
        stp.Page("buecher.py", "Bücher", ":books:"),
        stp.Page("schueler.py", "Schüler", ":student:"),
        stp.Page("gruppen.py", "Gruppen", ":man-woman-girl-girl:"),
        stp.Page("benotung.py", "Benotung", ":1234:")
    ]
    stp.show_pages(pages)
    

def login_pressed(name:str, password:str):
    # Load the credentials from the database
    db = DB()
    db_usernames, db_passwords = db.get_credentials()
    db.__del__()

    # Get the hexadecimal representation of the hashed password
    hashed_password = hash(password)

    if name in db_usernames and hashed_password == db_passwords[db_usernames.index(name)]:
        st.session_state.logged_in = True
        
    else:
        st.error("The name or password you entered is incorrect.")

def login():
    st.title("Login Page")
    # Insert a form
    name = st.text_input("Name")
    password = st.text_input("Password", type="password")
    st.button("Login", on_click=lambda: login_pressed(name, password))
    
    
# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
else:
    main()
