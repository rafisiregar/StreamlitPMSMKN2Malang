import streamlit as st  # type:ignore
import sidebar as sd
import pklsmk2 
import home

# Set page config
st.set_page_config(page_title="Penempatan PKL SMK Negeri 2 Malang", layout="wide", initial_sidebar_state="expanded")
page = sd.render_sidebar()

if page == "Home":
    home.show()
elif page == "PKL Placement":
    pklsmk2.show()  
else:
    pass
