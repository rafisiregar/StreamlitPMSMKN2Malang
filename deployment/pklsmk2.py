import pickle
import streamlit as st #type:ignore
import pandas as pd
import os

# Fungsi untuk memuat model pickle
def load_model():
    model_path = os.path.join(os.path.dirname(__file__), "..", "deployment", "pkl_placement_model.pkl")
    try:
        # Pastikan model pickle dapat dimuat dengan benar
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        st.success("Model berhasil dimuat!")
        return model
    except FileNotFoundError:
        st.error(f"File model tidak ditemukan di: {model_path}")
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

# Fungsi untuk menjalankan antarmuka Streamlit
def show():
    # Memuat model hanya sekali saat aplikasi dijalankan
    model = load_model()
    if model is None:
        return

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
