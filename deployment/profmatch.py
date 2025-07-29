import streamlit as st  # type:ignore
import pandas as pd
from pklplacementmodel import PKLPlacementModel
import io
import matplotlib.pyplot as plt
import plotly.express as px 

def show():

    # Initialize the model
    model = PKLPlacementModel()

    # Streamlit UI
    st.title("Profile Matching - PKL Placement")

    st.markdown("""
Please read the instructions in the Home page before proceeding!
""")
    
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

        # Strip spaces from column names in case they have extra spaces
        df.columns = df.columns.str.strip()

        # Step 3: Display the dataframe and check column names
        st.subheader("Data Preview")
        st.dataframe(df)

        # Step 4: Display the total number of students in the dataset
        st.write(f"Total students in the dataset: {len(df)}")
        
        # Step 5: Inference button
        if st.button("🔍 Prediksi!"):
            predictions = []

            # Step 6: Loop through all rows in the dataframe
            for index, row in df.iterrows():
                # Ensure the correct columns exist in the dataframe
                try:
                    sub_aspek_data = row[['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9', 'A10', 'A11']].values
                    # Ensure the data is in the correct format (list of floats)
                    sub_aspek_data = [float(value) for value in sub_aspek_data]
                except KeyError:
                    st.error("Kolom yang diperlukan tidak ditemukan di file. Pastikan file memiliki kolom A1 sampai A11.")
                    return

                # Run the inference
                total, kategori_terbaik = model.inference(sub_aspek_data)

                # Ambil nama kolom dari nilai pada baris A, B, dan N
                nisn = row.iloc[0]  # Kolom A (indeks 0)
                nama_lengkap = row.iloc[1]  # Kolom B (indeks 1)
                jurusan = row.iloc[13]  # Kolom N (indeks 13) (Kolom N adalah kolom ke-14 karena indeks mulai dari 0)


                # Prepare the result for this row
                predictions = {
                    row.iloc[0]: nisn,  # Dinamis, menggunakan nilai di row[0] sebagai nama kolom
                    row.iloc[1]: nama_lengkap,  # Dinamis, menggunakan nilai di row[1] sebagai nama kolom
                    row.iloc[13]: jurusan,  # Dinamis, menggunakan nilai di row[13] sebagai nama kolom
                    "Kategori Terbaik": kategori_terbaik,
                    "Total Nilai": total
                }

            # Step 7: Convert the predictions list into a dataframe
            result_df = pd.DataFrame(predictions)

            # Step 8: Display results
            st.subheader("Prediction Results")
            st.dataframe(result_df)

            # Step 9: Allow the user to input a custom filename for download
            custom_filename = st.text_input("Masukkan Nama File untuk Download tanpa ekstensi (contoh: PrediksiSiswaPKL)", "PrediksiSiswaPKL")

            if custom_filename:
                # Ensure the file name ends with .xlsx
                file_name = f"{custom_filename}.xlsx"

                # Save result as an Excel file
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine="openpyxl") as writer:
                    result_df.to_excel(writer, index=False, sheet_name="Prediction")
                output.seek(0)

                st.download_button(
                    label="Download Prediction Results",
                    data=output,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            # Step 10: Create interactive visualizations using Plotly

            # Pie chart for placement categories distribution
            fig1 = px.pie(result_df, 
                          names="Kategori Terbaik", 
                          color="Kategori Terbaik",
                          title="Placement Category Distribution", 
                          color_discrete_map={"Mobile Engineering": "lightcoral", 
                                              "Software Engineering": "lightgreen", 
                                              "Internet of Things": "lightblue"},
                          labels={"Kategori Terbaik": "Kategori Penempatan"})

            # Adjust plot size and font size
            fig1.update_layout(
                width=1000, height=700,  # Increase plot size
                title_font_size=24,
                legend_title_font_size=20,
                legend_font_size=20,
                font_size=20
            )
            # Add count labels to the pie chart
            category_counts = result_df["Kategori Terbaik"].value_counts()
            fig1.update_traces(textinfo="percent+label+value")
            st.plotly_chart(fig1)

            # **Fix for the bar chart - Count the students per Jurusan and Kategori Terbaik**
            count_df = result_df.groupby(['Jurusan', 'Kategori Terbaik']).size().reset_index(name='Total Siswa')

            # Create the bar chart with correct count of students
            fig2 = px.bar(count_df, 
                          x="Jurusan", 
                          y="Total Siswa", 
                          color="Kategori Terbaik", 
                          title="Number of Students by Class and Placement Category",       
                          labels={"Jurusan": "Class", "Kategori Terbaik": "PKL Placement Category", "Total Siswa":"Total Students"},
                          category_orders={"Kategori Terbaik": ["Mobile Engineering", "Software Engineering", "Internet of Things"]},
                          color_discrete_map={"Mobile Engineering": "lightcoral", 
                                              "Software Engineering": "lightgreen", 
                                              "Internet of Things": "lightblue"})

            # Adjust plot size and font size
            fig2.update_layout(
                width=1000, height=700,  # Increase plot size
                title_font_size=24,
                xaxis_title_font_size=20,
                yaxis_title_font_size=20,
                legend_title_font_size=20,
                legend_font_size=20,
                font_size=20
            )

            # Add count labels on bars
            fig2.update_traces(texttemplate='%{y}', textposition='outside', cliponaxis=False)

            st.plotly_chart(fig2)

if __name__ == "__main__":
    show()
