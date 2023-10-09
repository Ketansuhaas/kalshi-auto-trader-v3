import streamlit as st
from Login import *

if 'username' in st.session_state and 'password' in st.session_state:
    date = st.date_input("Enter Today's Date")
    if date is not None:
        st.session_state['date'] = date
    if 'date' in st.session_state:
        st.text('Fetching Data...')
        df = get_data(date)
        st.text('Data fetching process complete.')
        complexity = st.text_input('Enter VAR model complexity (preferably 170)')
        if complexity:
            st.session_state['pred'] = build_predict(df,int(complexity))
            st.text(f"VAR Model Predicted Today's High Temperature as {st.session_state['pred']}")
            st.text('Open Trade page')
else:
    st.text('Please Login first')