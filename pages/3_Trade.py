import streamlit as st
from Login import *
    
if 'username' in st.session_state and 'password' in st.session_state and 'pred' in st.session_state:
    ticker,ex = get_suitable_ticker(st.session_state['pred'],st.session_state['username'],st.session_state['password'],st.session_state['date'])
    st.text(f"Suitable market: {ticker}")
    st.text(f"Available balance in cents: {ex.get_balance()['balance']}")
    contracts = st.text_input('No. of contracts')
    price = st.text_input('Price limit in cents')
    if contracts!="" and price!="":
        st.session_state['contracts'] = int(contracts)
        st.session_state['price'] = int(price)
        if st.button('Trade?'):
            st.text(f'Initiating trade for {st.session_state['contracts']} contracts')
            st.text('Trade in progress...')
            make_trade(ticker,ex,st.session_state['contracts'],st.session_state['price'])
            st.text('Trade successfully completed')
    else:
        st.text('Enter contracts and price limit')
else:
    st.text('Please login and train the model first')
