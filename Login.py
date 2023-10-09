import streamlit as st
from KalshiClientsBaseV2 import ExchangeClient
from Script import *

st.title('Kalshi Auto-Trader')
username = st.text_input('Kalshi username:')
password = st.text_input('Kalshi password:',type = "password")

if username!="" and password!="":
    st.session_state['username'] = username
    st.session_state['password'] = password

if 'username' in st.session_state and 'password' in st.session_state:
    st.text("Logged in, go ahead and train the model")
    ex = ExchangeClient(exchange_api_base = "https://demo-api.kalshi.co/trade-api/v2", \
                        email = st.session_state['username'], password = st.session_state['password'])
    st.text(f"Status: {ex.get_exchange_status()}")
        

