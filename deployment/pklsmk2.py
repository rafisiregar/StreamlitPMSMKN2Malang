# type: ignore
import streamlit as st
import numpy as np
import pandas as pd
import pickle
import os
import pickle

# Simpan model ke file pickle
with open('pkl_placement_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Memuat model
with open('pkl_placement_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Streamlit UI
def show():
    # Path ke file model pickle yang sudah disimpan
    try:
        model_path = os.path.join(os.path.dirname(__file__), "..", "deployment", "pkl_placement_model.pkl")
        with open(model_path, "rb") as f:
            model = pickle.load(f)  # Memuat model pickle
        st.success("Model berhasil dimuat!")
    except FileNotFoundError:
        st.error("File model tidak ditemukan!")
        return
    except Exception as e:
        st.error(f"Terjadi kesalahan saat memuat model: {e}")
        return

    st.title("🔍 Profile Matching for PKL Placement")

    # First inference - Profile Matching (similar to previous)
    st.markdown("### 1. Prediksi Penempatan PKL Berdasarkan Data Sub-Aspek")
    st.markdown("Unggah data sub-aspek untuk memprediksi penempatan PKL berdasarkan **Mobile Engineering**, **Software Engineering**, atau **Internet of Things**.")
    
    uploaded_file = st.file_uploader("📤 Upload file data (Excel format)", type=["xlsx"])
    

    if uploaded_file:
        st.subheader("📊 Data yang Diunggah")
        # Read Excel file to show sheet names
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            st.write("Pilih sheet yang ingin digunakan:")
            sheet_name = st.selectbox("Sheet", excel_file.sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            st.dataframe(df.head())  # Show a preview of the data
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return

        st.markdown("### 📝 Pilih label sebenarnya (aktual):")
        pkl_labels = ["Mobile Engineering", "Software Engineering", "Internet of Things"]
        selected_label = st.radio("Pilih kategori aktual PKL:", options=pkl_labels)

        if st.button("🔍 Submit & Prediksi"):
            # Validate data and run inference
            if df.shape[1] < 11:
                st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                return

            sub_aspek_data = df.iloc[0, :11].values  # Assuming the first row contains the sub-aspect values
            sub_aspek_data = sub_aspek_data.tolist()

            # Make prediction
            total, predicted_label = model.inference(sub_aspek_data)

            # Output the prediction
            st.markdown("### 📌 Hasil Prediksi Model")
            st.success(f"**Penempatan PKL yang Direkomendasikan:** {predicted_label}")
            st.info(f"**Nilai Total Prediksi:** {total:.2f}")

            # Show actual label (Ground truth)
            st.markdown("---")
            st.markdown("### ✅ Hasil Aktual Data")
            st.success(f"**Penempatan PKL Sebenarnya:** {selected_label}")

            # Compare prediction with the actual label
            if predicted_label.lower() == selected_label.lower():
                st.success("✅ Prediksi sesuai dengan label yang dipilih.")
            else:
                st.error("❌ Prediksi tidak sesuai dengan label yang dipilih.")

    # Second inference - Add new column to the Excel sheet with PKL placement prediction
    st.markdown("### 2. Menambahkan Hasil Penempatan PKL ke File Excel")
    st.markdown("Unggah file Excel yang memiliki data sub-aspek, pilih sheet, dan hasil penempatan akan ditambahkan ke kolom baru dalam file yang sama.")

    uploaded_file_2 = st.file_uploader("📤 Upload file data (Excel format) untuk menambah kolom hasil penempatan", type=["xlsx"])

    if uploaded_file_2:
        try:
            excel_file_2 = pd.ExcelFile(uploaded_file_2)
            st.write("Pilih sheet yang ingin digunakan:")
            sheet_name_2 = st.selectbox("Sheet", excel_file_2.sheet_names)
            df_2 = pd.read_excel(uploaded_file_2, sheet_name=sheet_name_2)
            st.dataframe(df_2.head())  # Show a preview of the data
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return

        if st.button("🔍 Submit & Tambah Hasil Penempatan"):
            # Validate data
            if df_2.shape[1] < 11:
                st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                return

            # Predict PKL placement for each row based on sub-aspect data (A1, A2, ..., A11)
            results = []
            for idx, row in df_2.iterrows():
                sub_aspek_data = row[:11].values  # Assuming the first 11 columns are sub-aspects
                sub_aspek_data = sub_aspek_data.tolist()
                total, predicted_label = model.inference(sub_aspek_data)
                results.append(predicted_label)

            # Add the prediction results as a new column
            df_2['Hasil Penempatan'] = results

            # Show the dataframe with the new column
            st.markdown("### Hasil Data dengan Kolom 'Hasil Penempatan' yang Ditambahkan:")
            st.dataframe(df_2.head())  # Show the updated dataframe

            # Save the updated dataframe to a new file
            output_file = "/mnt/data/updated_pkl_placement_result.xlsx"
            df_2.to_excel(output_file, index=False)
            st.download_button(
                label="Download File dengan Hasil Penempatan",
                data=open(output_file, 'rb'),
                file_name="updated_pkl_placement_result.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

# Run
if __name__ == "__main__":
    show()
