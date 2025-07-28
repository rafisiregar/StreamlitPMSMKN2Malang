import streamlit as st #type:ignore
import pandas as pd
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

# Fungsi utama untuk menjalankan aplikasi Streamlit
def show():
    # Inisialisasi model PKLPlacementModel
    model = PKLPlacementModel()

    st.title("🔍 Profile Matching for PKL Placement")

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

if __name__ == "__main__":
    show()
