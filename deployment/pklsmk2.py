import streamlit as st  # type: ignore
import pandas as pd
import openpyxl
import tempfile
from pklplacementmodel import PKLPlacementModel  # Import model

# Fungsi untuk membaca file Excel
def read_excel_file(uploaded_file):
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Pilih sheet", excel_file.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None

def manual_inference():
    st.title("🔍 Manual Profile Matching for PKL Placement")
    model = PKLPlacementModel()

    # Input fields for A1 to A11
    A1 = st.number_input("Informatika (A1)", min_value=0, max_value=100, step=1)
    A2 = st.number_input("Dasar Program Keahlian (A2)", min_value=0, max_value=100, step=1)
    A3 = st.number_input("Projek Kreatif dan Kewirausahaan (A3)", min_value=0, max_value=100, step=1)
    A4 = st.number_input("Perencanaan dan Pengalamatan Jaringan (A4)", min_value=0, max_value=100, step=1)
    A5 = st.number_input("Administrasi Sistem Jaringan (A5)", min_value=0, max_value=100, step=1)
    A6 = st.number_input("Teknologi Jaringan Kabel dan Nirkabel (A6)", min_value=0, max_value=100, step=1)
    A7 = st.number_input("Pemasangan dan Konfigurasi Perangkat Jaringan (A7)", min_value=0, max_value=100, step=1)
    A8 = st.number_input("Samsung Tech Institute (A8)", min_value=0, max_value=100, step=1)
    A9 = st.number_input("Pemrograman Web (A9)", min_value=0, max_value=100, step=1)
    A10 = st.number_input("Internet of Things (A10)", min_value=0, max_value=100, step=1)
    A11 = st.number_input("Jarak (A11)", min_value=0, max_value=100, step=1)

    # Button to trigger the inference
    if st.button("🔍 Lakukan Prediksi Manual"):
        # Collect input data
        sub_aspek_data = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]
        try:
            total, predicted_label = model.inference(sub_aspek_data)
            st.subheader(f"Hasil Prediksi: {predicted_label}")
        except Exception as e:
            st.error(f"Error during prediction: {e}")

# Fungsi utama untuk menjalankan aplikasi Streamlit
def show():
    st.title("🔍 Profile Matching for PKL Placement")

    menu = ["Upload File", "Manual Input"]
    choice = st.sidebar.selectbox("Pilih Mode", menu)

    if choice == "Upload File":
        uploaded_file = st.file_uploader("📤 Upload file data (Excel format)", type=["xlsx"])
        
        if uploaded_file:
            df = read_excel_file(uploaded_file)
            if df is not None:
                st.subheader("📊 Data yang Diunggah")
                st.dataframe(df.head())  # Menampilkan preview dari data yang diupload

                # Pastikan data memiliki minimal 11 kolom (A1-A11)
                if df.shape[1] < 11:
                    st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                    return

                # Inisialisasi model PKLPlacementModel
                model = PKLPlacementModel()

                # Pemetaan sub-aspek ke kode A1-A11
                sub_aspek_mapping = model.map_sub_aspek_to_kode()

                # Menampilkan pemetaan sub-aspek ke kode
                st.subheader("Pemetaan Sub-Aspek ke Kode:")
                st.write(sub_aspek_mapping)

                # Tombol untuk memulai prediksi
                if st.button("🔍 Lakukan Prediksi"):
                    predictions = []  # Menyimpan hasil prediksi untuk setiap baris
                    for index, row in df.iterrows():
                        sub_aspek_data = row[:11].values.tolist()  # Mengambil data A1-A11
                        try:
                            total, predicted_label = model.inference(sub_aspek_data)
                            predictions.append(predicted_label)  # Menyimpan label prediksi
                        except Exception as e:
                            predictions.append("Error")  # Jika terjadi error, simpan 'Error'

                    # Menambahkan hasil prediksi ke dataframe
                    df['Penempatan PKL'] = predictions

                    # Menyimpan hasil dataframe ke dalam file Excel sementara
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
                        output_file = tmpfile.name
                        df.to_excel(output_file, index=False)

                    # Menampilkan tombol download untuk file yang telah diperbarui
                    st.download_button(
                        label="Download File dengan Hasil Penempatan",
                        data=open(output_file, 'rb'),
                        file_name="updated_pkl_placement_result.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

    elif choice == "Manual Input":
        manual_inference()

if __name__ == "__main__":
    show()
