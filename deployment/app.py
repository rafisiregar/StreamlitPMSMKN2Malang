import streamlit as st  # type: ignore
import sidebar as sd  
import profmatch
import home  
import tryon

# Set page config (pastikan ini hanya dipanggil sekali)
st.set_page_config(page_title="Penempatan PKL SMK Negeri 2 Malang", layout="wide", initial_sidebar_state="expanded")

# Render sidebar dan pilih halaman
page = sd.render_sidebar()

# Menentukan halaman berdasarkan pilihan pengguna
if page == "Home":
    home.show() 
elif page == "PKL Placement":
    # Display PKL Placement page content
    profmatch.show()
elif page == "Try On!":
    # Display PKL Placement page content
    tryon.show() 
else:
    pass
