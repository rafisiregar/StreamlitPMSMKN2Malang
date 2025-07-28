import streamlit as st #type:ignore
import pandas as pd
from pklplacementmodel import PKLPlacementModel
import io

def show():
    # Initialize the model
    model = PKLPlacementModel()

    # Streamlit UI
    st.title("Profile Matching - PKL Placement")

    # Step 1: File upload
    uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx"])

    if uploaded_file is not None:
        # Read the Excel file
        excel_data = pd.ExcelFile(uploaded_file)

        # Step 2: Display sheets for the user to select
        sheet_names = excel_data.sheet_names
        selected_sheet = st.selectbox("Select a sheet", sheet_names)

        # Load data from selected sheet
        df = excel_data.parse(selected_sheet)

        # Step 3: Display the dataframe
        st.subheader("Data Preview")
        st.dataframe(df)

        # Step 4: Inference button
        if st.button("🔍 Prediksi!"):
            # Step 5: Run the inference
            sub_aspek_data = df.values[0]  # Assumes the first row contains the relevant data for inference
            total, kategori_terbaik = model.inference(sub_aspek_data)

            # Step 6: Display results
            st.subheader("Hasil Inference")
            result_df = pd.DataFrame({
                "Kategori Terbaik": [kategori_terbaik],
                "Total Nilai": [total]
            })
            st.dataframe(result_df)

            # Step 7: Allow the user to download the file with predictions
            download_file = result_df.copy()
            download_file["Nama File"] = kategori_terbaik + "_prediction.xlsx"
            
            # Save result as an Excel file
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                download_file.to_excel(writer, index=False, sheet_name="Prediction")
            output.seek(0)

            st.download_button(
                label="Download Hasil Prediksi",
                data=output,
                file_name=f"{kategori_terbaik}_prediction.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )