import streamlit as st
import pandas as pd

# Beispiel-Datenframe
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Alter': [25, 30, 35],
        'Stadt': ['Berlin', 'München', 'Hamburg']}

df = pd.DataFrame(data)

# Haupttabelle anzeigen
main_table = st.table(df)

# Index der ausgewählten Zelle
selected_cell = st.table({})

# Überprüfen, ob eine Zelle in der Haupttabelle ausgewählt wurde
if main_table.button('Zelle auswählen'):
    selected_cell = st.table({'Selected Cell': [main_table.selected_row, main_table.selected_col]})

# Überprüfen, ob eine Detailseite angezeigt werden soll
if selected_cell:
    # Hier können Sie die Detailseite basierend auf den ausgewählten Zellinformationen erstellen
    st.write(f'Detailseite für Zelle: {selected_cell}')
