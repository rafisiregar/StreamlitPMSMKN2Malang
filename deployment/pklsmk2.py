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

    # Function to clean and validate data
    def clean_data(df):
        # Convert the first 11 columns to numeric, coercing errors (non-numeric values will become NaN)
        df_cleaned = df.iloc[:, :11].apply(pd.to_numeric, errors='coerce')
        
        # Check if there are any NaN values after conversion
        if df_cleaned.isnull().values.any():
            st.warning("Beberapa nilai dalam data tidak valid (misalnya kosong atau teks). Nilai tersebut akan diperlakukan sebagai NaN.")
            # Handle missing data (NaN), either fill with default value (like 0 or mean) or drop the rows
            df_cleaned = df_cleaned.fillna(0)  # Or use df_cleaned.dropna() to remove rows with NaN
        return df_cleaned

    # Instantiate the model once when the app starts
    model = PKLPlacementModel()  # Instantiate the PKLPlacementModel

    st.title("🔍 Profile Matching for PKL Placement")

    # First inference - Profile Matching
    st.markdown("### Prediksi Penempatan PKL")
    st.markdown("Unggah data sub-aspek untuk memprediksi penempatan PKL berdasarkan **Mobile Engineering**, **Software Engineering**, atau **Internet of Things**.")
    
    uploaded_file = st.file_uploader("📤 Upload file data (Excel format)", type=["xlsx"])

    if uploaded_file:
        df = read_excel_file(uploaded_file)
        if df is not None:
            st.subheader("📊 Data yang Diunggah")
            st.dataframe(df.head())  # Display a preview of the uploaded data

            # Ensure that the data has at least 11 columns (A1-A11)
            if df.shape[1] < 11:
                st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
                return

            # Clean the data by converting to numeric and handling missing values
            df_cleaned = clean_data(df)

            # Select actual PKL label
            st.markdown("### 📝 Pilih label sebenarnya (aktual):")
            pkl_labels = ["Mobile Engineering", "Software Engineering", "Internet of Things"]
            selected_label = st.radio("Pilih kategori aktual PKL:", options=pkl_labels)

            # Button to submit and make predictions
            if st.button("🔍 Submit & Prediksi"):
                # Reading the first row of cleaned data (A1-A11 columns) for inference
                sub_aspek_data = df_cleaned.iloc[0, :11].values  # Take data from the first row
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

                    # Adding prediction result as a new column to the dataframe
                    df['Penempatan PKL'] = predicted_label

                    # Save the dataframe with the new prediction column to a new file
                    output_file = "/mnt/data/updated_pkl_placement_result.xlsx"
                    df.to_excel(output_file, index=False)

                    # Provide download button for the updated file
                    st.download_button(
                        label="Download File dengan Hasil Penempatan",
                        data=open(output_file, 'rb'),
                        file_name="updated_pkl_placement_result.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

                except Exception as e:
                    st.error(f"Terjadi kesalahan saat melakukan prediksi: {e}")

if __name__ == "__main__":
    show()
