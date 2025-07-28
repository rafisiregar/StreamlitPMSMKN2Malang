import streamlit as st  # type:ignore
import openpyxl
import pandas as pd  # Make sure pandas is imported
from pklplacementmodel import PKLPlacementModel  # Import the model class from pklplacementmodel.py

# Main function to run the Streamlit app
def show():

    # Function to read Excel files
    def read_excel_file(uploaded_file):
        try:
            excel_file = pd.ExcelFile(uploaded_file)
            sheet_name = st.selectbox("Pilih sheet", excel_file.sheet_names)
            df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
            return df
        except Exception as e:
            st.error(f"Error reading the Excel file: {e}")
            return None

    # Instantiate the model once when the app starts
    model = PKLPlacementModel()  # Instantiate the PKLPlacementModel

    st.title("🔍 Profile Matching for PKL Placement")

    # First inference - Profile Matching
    st.markdown("### 1. Prediksi Penempatan PKL Berdasarkan Data Sub-Aspek")
    st.markdown("Unggah data sub-aspek untuk memprediksi penempatan PKL berdasarkan **Mobile Engineering**, **Software Engineering**, atau **Internet of Things**.")
    
    uploaded_file = st.file_uploader("📤 Upload file data (Excel format)", type=["xlsx"])

    if uploaded_file:
        df = read_excel_file(uploaded_file)
        if df is not None:
            st.subheader("📊 Data yang Diunggah")
            st.dataframe(df.head())  # Display a preview of the uploaded data

            st.markdown("### 📝 Pilih label sebenarnya (aktual):")
            pkl_labels = ["Mobile Engineering", "Software Engineering", "Internet of Things"]
            selected_label = st.radio("Pilih kategori aktual PKL:", options=pkl_labels)

            if st.button("🔍 Submit & Prediksi"):
                # Validate data and run inference
                if df.shape[1] < 11:
                    st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                    return

                sub_aspek_data = df.iloc[0, :11].values  # Take data from the first row
                sub_aspek_data = sub_aspek_data.tolist()

                try:
                    # Perform prediction using the model
                    total, predicted_label = model.inference(sub_aspek_data)

                    # Display prediction result
                    st.markdown("### 📌 Hasil Prediksi Model")
                    st.success(f"**Penempatan PKL yang Direkomendasikan:** {predicted_label}")
                    st.info(f"**Nilai Total Prediksi:** {total:.2f}")

                    # Display the actual label (Ground truth)
                    st.markdown("---")
                    st.markdown("### ✅ Hasil Aktual Data")
                    st.success(f"**Penempatan PKL Sebenarnya:** {selected_label}")

                    # Compare predicted label with actual label
                    if predicted_label.lower() == selected_label.lower():
                        st.success("✅ Prediksi sesuai dengan label yang dipilih.")
                    else:
                        st.error("❌ Prediksi tidak sesuai dengan label yang dipilih.")
                except Exception as e:
                    st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

    # Second inference - Add PKL placement results to the Excel file
    st.markdown("### 2. Menambahkan Hasil Penempatan PKL ke File Excel")
    st.markdown("Unggah file Excel yang memiliki data sub-aspek, pilih sheet, dan hasil penempatan akan ditambahkan ke kolom baru dalam file yang sama.")

    uploaded_file_2 = st.file_uploader("📤 Upload file data (Excel format) untuk menambah kolom hasil penempatan", type=["xlsx"])

    if uploaded_file_2:
        df_2 = read_excel_file(uploaded_file_2)
        if df_2 is not None:
            st.subheader("📊 Data yang Diunggah")
            st.dataframe(df_2.head())  # Display a preview of the uploaded data

            if st.button("🔍 Submit & Tambah Hasil Penempatan"):
                # Validate data
                if df_2.shape[1] < 11:
                    st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                    return

                # Predict PKL placement for each row based on sub-aspect data (A1, A2, ..., A11)
                results = []
                for idx, row in df_2.iterrows():
                    sub_aspek_data = row[:11].values  # Take data from the first 11 columns
                    sub_aspek_data = sub_aspek_data.tolist()
                    total, predicted_label = model.inference(sub_aspek_data)
                    results.append(predicted_label)

                # Add prediction results as a new column
                df_2['Hasil Penempatan'] = results

                # Display the updated data
                st.markdown("### Hasil Data dengan Kolom 'Hasil Penempatan' yang Ditambahkan:")
                st.dataframe(df_2.head())  # Display the updated dataframe

                # Save the updated dataframe to a new file
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
