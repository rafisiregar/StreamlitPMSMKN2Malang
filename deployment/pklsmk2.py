import streamlit as st #ignore: type
import pandas as pd
import tempfile
from pklplacementmodel import PKLPlacementModel  # Import model

# Constants
SUB_ASPECTS = [
    "Informatika (A1)",
    "Dasar Program Keahlian (A2)",
    "Projek Kreatif dan Kewirausahaan (A3)",
    "Perencanaan dan Pengalamatan Jaringan (A4)",
    "Administrasi Sistem Jaringan (A5)",
    "Teknologi Jaringan Kabel dan Nirkabel (A6)",
    "Pemasangan dan Konfigurasi Perangkat Jaringan (A7)",
    "Samsung Tech Institute (A8)",
    "Pemrograman Web (A9)",
    "Internet of Things (A10)",
    "Jarak (A11)"
]

def read_excel_file(uploaded_file):
    """Read and validate the uploaded Excel file."""
    try:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Pilih sheet", excel_file.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
        
        # Validate the dataframe
        if df.shape[1] < 11:
            st.error("Data tidak lengkap! Harap unggah data dengan minimal 11 kolom sub-aspek.")
            return None
            
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")
        return None

def process_file_upload(uploaded_file):
    """Process the uploaded file and return predictions."""
    df = read_excel_file(uploaded_file)
    if df is None:
        return None
        
    st.subheader("📊 Data yang Diunggah")
    st.dataframe(df.head())  # Show data preview

    model = PKLPlacementModel()
    predictions = []
    
    with st.spinner("Sedang memproses data..."):
        for index, row in df.iterrows():
            sub_aspek_data = row[:11].values.tolist()  # Get A1-A11 data
            try:
                total, predicted_label = model.inference(sub_aspek_data)
                predictions.append(predicted_label)
            except Exception as e:
                st.error(f"Error processing row {index}: {e}")
                predictions.append("Error")

    df['Penempatan PKL'] = predictions
    
    # Create downloadable file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmpfile:
        output_file = tmpfile.name
        df.to_excel(output_file, index=False)
    
    return output_file

def show_manual_input():
    """Show manual input form and process results."""
    st.subheader("Input Manual")
    
    inputs = []
    for i, aspect in enumerate(SUB_ASPECTS):
        inputs.append(st.number_input(aspect, min_value=0, max_value=100, step=1, key=f"input_{i}"))
    
    if st.button("🔍 Lakukan Prediksi Manual", key="manual_predict"):
        model = PKLPlacementModel()
        try:
            total, predicted_label = model.inference(inputs)
            st.success(f"Hasil Prediksi: {predicted_label}")
            st.write(f"Total Skor: {total}")
        except Exception as e:
            st.error(f"Error during prediction: {e}")

def main():
    """Main application function."""
    st.set_page_config(page_title="PKL Placement", layout="wide")
    
    st.title("🔍 Profile Matching for PKL Placement")
    st.write("Aplikasi ini membantu menentukan penempatan PKL yang sesuai berdasarkan profil akademik siswa.")
    
    # Sidebar navigation
    st.sidebar.title("Navigasi")
    mode = st.sidebar.radio("Pilih Mode", ["Upload File", "Manual Input"])
    
    if mode == "Upload File":
        st.subheader("Upload File Excel")
        uploaded_file = st.file_uploader(
            "📤 Upload file data (Excel format)", 
            type=["xlsx"],
            help="Unggah file Excel dengan minimal 11 kolom sub-aspek (A1-A11)"
        )
        
        if uploaded_file:
            output_file = process_file_upload(uploaded_file)
            if output_file:
                st.success("Proses prediksi selesai!")
                st.download_button(
                    label="📥 Download File dengan Hasil Penempatan",
                    data=open(output_file, 'rb'),
                    file_name="hasil_penempatan_pkl.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
    else:
        show_manual_input()

if __name__ == "__main__":
    main()