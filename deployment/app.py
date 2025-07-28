import streamlit as st  # type: ignore
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
    # Display PKL Placement page content
    pklsmk2.show()  
    
    # Check if manual_inference() function is properly defined and displayed
    try:
        pklsmk2.manual_inference()  # Call manual_inference function here
    except Exception as e:
        st.error(f"Error occurred in manual_inference: {e}")
else:
    pass
