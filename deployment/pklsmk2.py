import pickle
import streamlit as st  # type:ignore
import pandas as pd  # Pastikan pandas diimpor
import os

# Fungsi utama untuk menjalankan aplikasi Streamlit
def show():
    # Fungsi untuk memuat model pickle
    def load_model():
        model_path = os.path.join(os.path.dirname(__file__), "..", "deployment", "pkl_placement_model.pkl")
        try:
            with open(model_path, "rb") as f:
                model = pickle.load(f)  # Memuat model
            st.success("Model berhasil dimuat!")
            return model
        except FileNotFoundError:
            st.error("File model tidak ditemukan!")
            return None
        except AttributeError as e:
            st.error(f"Terjadi kesalahan: Model tidak dapat dimuat karena masalah atribut: {e}")
            return None
        except Exception as e:
            st.error(f"Terjadi kesalahan saat memuat model: {e}")
            return None

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

    # Memuat model hanya sekali saat aplikasi dijalankan
    model = load_model()
    if model is None:
        return  # Jika model tidak dimuat, hentikan eksekusi lebih lanjut.

    st.title("🔍 Profile Matching for PKL Placement")

    # First inference - Profile Matching
    st.markdown("### 1. Prediksi Penempatan PKL Berdasarkan Data Sub-Aspek")
    st.markdown("Unggah data sub-aspek untuk memprediksi penempatan PKL berdasarkan **Mobile Engineering**, **Software Engineering**, atau **Internet of Things**.")
    
    uploaded_file = st.file_uploader("📤 Upload file data (Excel format)", type=["xlsx"])

    if uploaded_file:
        df = read_excel_file(uploaded_file)
        if df is not None:
            st.subheader("📊 Data yang Diunggah")
            st.dataframe(df.head())  # Menampilkan preview data

            st.markdown("### 📝 Pilih label sebenarnya (aktual):")
            pkl_labels = ["Mobile Engineering", "Software Engineering", "Internet of Things"]
            selected_label = st.radio("Pilih kategori aktual PKL:", options=pkl_labels)

            if st.button("🔍 Submit & Prediksi"):
                # Validasi data dan jalankan inferensi
                if df.shape[1] < 11:
                    st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                    return

                sub_aspek_data = df.iloc[0, :11].values  # Mengambil data dari baris pertama
                sub_aspek_data = sub_aspek_data.tolist()

                try:
                    # Lakukan prediksi menggunakan model
                    # Pastikan metode inference ada pada model Anda
                    if hasattr(model, 'inference'):
                        total, predicted_label = model.inference(sub_aspek_data)
                    else:
                        st.error("Model tidak memiliki metode inference yang valid.")
                        return

                    # Output hasil prediksi
                    st.markdown("### 📌 Hasil Prediksi Model")
                    st.success(f"**Penempatan PKL yang Direkomendasikan:** {predicted_label}")
                    st.info(f"**Nilai Total Prediksi:** {total:.2f}")

                    # Menampilkan label aktual (Ground truth)
                    st.markdown("---")
                    st.markdown("### ✅ Hasil Aktual Data")
                    st.success(f"**Penempatan PKL Sebenarnya:** {selected_label}")

                    # Bandingkan prediksi dengan label aktual
                    if predicted_label.lower() == selected_label.lower():
                        st.success("✅ Prediksi sesuai dengan label yang dipilih.")
                    else:
                        st.error("❌ Prediksi tidak sesuai dengan label yang dipilih.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

    # Second inference - Menambahkan hasil penempatan PKL ke file Excel
    st.markdown("### 2. Menambahkan Hasil Penempatan PKL ke File Excel")
    st.markdown("Unggah file Excel yang memiliki data sub-aspek, pilih sheet, dan hasil penempatan akan ditambahkan ke kolom baru dalam file yang sama.")

    uploaded_file_2 = st.file_uploader("📤 Upload file data (Excel format) untuk menambah kolom hasil penempatan", type=["xlsx"])

    if uploaded_file_2:
        df_2 = read_excel_file(uploaded_file_2)
        if df_2 is not None:
            st.subheader("📊 Data yang Diunggah")
            st.dataframe(df_2.head())  # Menampilkan preview data

            if st.button("🔍 Submit & Tambah Hasil Penempatan"):
                # Validasi data
                if df_2.shape[1] < 11:
                    st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                    return

                # Prediksi penempatan PKL untuk setiap baris berdasarkan data sub-aspek (A1, A2, ..., A11)
                results = []
                for idx, row in df_2.iterrows():
                    sub_aspek_data = row[:11].values  # Mengambil data dari 11 kolom pertama
                    sub_aspek_data = sub_aspek_data.tolist()
                    total, predicted_label = model.inference(sub_aspek_data)
                    results.append(predicted_label)

                # Menambahkan hasil prediksi sebagai kolom baru
                df_2['Hasil Penempatan'] = results

                # Menampilkan data yang telah diperbarui
                st.markdown("### Hasil Data dengan Kolom 'Hasil Penempatan' yang Ditambahkan:")
                st.dataframe(df_2.head())  # Menampilkan dataframe yang diperbarui

                # Menyimpan dataframe yang sudah diperbarui ke file baru
                output_file = "/mnt/data/updated_pkl_placement_result.xlsx"
                df_2.to_excel(output_file, index=False)
                st.download_button(
                    label="Download File dengan Hasil Penempatan",
                    data=open(output_file, 'rb'),
                    file_name="updated_pkl_placement_result.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )  

if __name__ == "__main__":
    show()
