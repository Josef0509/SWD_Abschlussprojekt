import streamlit as st
import numpy as np
import pandas as pd

from st_aggrid import AgGrid, DataReturnMode, GridUpdateMode, GridOptionsBuilder, JsCode

@st.cache()
def generate_df():
    df = pd.DataFrame(
        np.random.randint(0, 100, 30).reshape(-1, 3), columns=list("abc")
    )
    return df

data = generate_df()


gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_columns(list('abc'), editable=True)


js = JsCode("""
function(e) {
    let api = e.api;
    let rowIndex = e.rowIndex;
    let col = e.column.colId;
    
    let rowNode = api.getDisplayedRowAtIndex(rowIndex);
    
    console.log("column index: " + col + ", row index: " + rowIndex);
};
""")

gb.configure_grid_options(onCellClicked=js)
gb.configure_selection(selection_mode ='single')
go = gb.build()

return_ag = AgGrid(data, gridOptions=go, allow_unsafe_jscode=True, reload_data=False, update_mode=GridUpdateMode.SELECTION_CHANGED)

print(return_ag)