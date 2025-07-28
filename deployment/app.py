import streamlit as st #type:ignore
import sidebar as sd  # Pastikan file sidebar.py ada
import pklsmk2  # Pastikan pklsmk2.py ada dan memiliki fungsi show()
import home  # Pastikan home.py ada dan memiliki fungsi show()

# Set page config (pastikan ini hanya dipanggil sekali)
st.set_page_config(page_title="Penempatan PKL SMK Negeri 2 Malang", layout="wide", initial_sidebar_state="expanded")

# Render sidebar dan pilih halaman
page = sd.render_sidebar()

# Menentukan halaman berdasarkan pilihan pengguna
if page == "Home":
    home.show()  # Memanggil fungsi show() dari home.py
elif page == "PKL Placement":
    pklsmk2.show()  # Memanggil fungsi show() dari pklsmk2.py
else:
    pass  # Jika tidak ada pilihan yang cocok, tidak perlu melakukan apapun
