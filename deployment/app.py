import streamlit as st # type:ignore
import sidebar as sd

# Set page config
st.set_page_config(page_title="Penempatan PKL SMK Negeri 2 Malang", layout="wide", initial_sidebar_state="expanded")
page = sd.render_sidebar()

import profilematching 
import home 

if page == "Home":
    home.show()
elif page == "Prediction":
    profilematching.show()
