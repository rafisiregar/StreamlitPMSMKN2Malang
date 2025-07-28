import streamlit as st #type:ignore
import sidebar as sd  
import pklsmk2
import home  

# Set page config (pastikan ini hanya dipanggil sekali)
st.set_page_config(page_title="Penempatan PKL SMK Negeri 2 Malang", layout="wide", initial_sidebar_state="expanded")

# Render sidebar dan pilih halaman
page = sd.render_sidebar()

# Menentukan halaman berdasarkan pilihan pengguna
if page == "Home":
    home.show() 
elif page == "PKL Placement":
    pklsmk2.show()
    pklsmk2.manual_inference() 
else:
    pass  
