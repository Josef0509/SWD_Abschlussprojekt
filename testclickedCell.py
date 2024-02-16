import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

def main():
    st.title("Clickable Table with AgGrid in Streamlit")

    # Sample data
    data = pd.DataFrame({
        "Column 1": ["Data 1", "Data 2", "Data 3"],
        "Column 2": ["Data 4", "Data 5", "Data 6"],
        "Column 3": ["Data 7", "Data 8", "Data 9"]
    })

    # Display the table using st.aggrid
    grid = st.aggrid(data)

    # Handle widget events
    event = st.get_last_widget_event()
    if event:
        if event["event"] == "cellClicked":
            clicked_row = event["data"]["row"]
            clicked_col = event["data"]["column"]
            st.write(f"Cell clicked: Row {clicked_row}, Column {clicked_col}")

if __name__ == "__main__":
    main()
