import streamlit as st  # type:ignore
from pklplacementmodel import PKLPlacementModel

def show():
    # Initialize the model
    model = PKLPlacementModel()

    # Streamlit UI
    st.title("Profile Matching Inference")

    st.markdown("""
    **Welcome to the Profile Matching Inference!**  
    Please input your data for predicting the best PKL placement based on your skills and academic performance.
    """)

    # Step 1: User inputs for each aspect (A1 to A11)
    st.subheader("Try Input Your Data for Predicting PKL Placement!")

    # Input for each sub-aspect (A1 to A11)
    A1 = st.number_input("Informatika (A1)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Informatics (Computer Science) subject")
    A2 = st.number_input("Dasar Program Keahlian (A2)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Basic Program Expertise subject")
    A3 = st.number_input("Projek Kreatif dan Kewirausahaan (A3)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Creative Projects and Entrepreneurship subject")
    A4 = st.number_input("Perencanaan dan Pengalamatan Jaringan (A4)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Network Planning and Addressing subject")
    A5 = st.number_input("Administrasi Sistem Jaringan (A5)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Network System Administration subject")
    A6 = st.number_input("Teknologi Jaringan Kabel dan Nirkabel (A6)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Cable and Wireless Network Technologies subject")
    A7 = st.number_input("Pemasangan dan Konfigurasi Perangkat Jaringan (A7)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Network Device Installation and Configuration subject")
    A8 = st.number_input("Samsung Tech Institute (A8)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Samsung Tech Certification subject")
    A9 = st.number_input("Pemrograman Web (A9)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Web Programming subject")
    A10 = st.number_input("Internet of Things (A10)", min_value=0.0, max_value=100.0, step=0.1, help="Score for IoT Technologies subject")
    A11 = st.number_input("Jarak (A11)", min_value=0.0, max_value=100.0, step=0.1, help="Score for Distance (specific to program)")

    # Allow null by using `None` if no input is provided
    A8 = None if A8 == 0.0 else A8
    A9 = None if A9 == 0.0 else A9
    A10 = None if A10 == 0.0 else A10
    
    # Store the inputs in a list
    sub_aspek_data = [A1, A2, A3, A4, A5, A6, A7, A8, A9, A10, A11]

    # Step 2: Inference button
    if st.button("🔍 Get Recommendation!"):
    # Check if A8, A9, A10 can be null but other fields must have a value greater than 0
        if all((value is not None and value > 0) for i, value in enumerate(sub_aspek_data) if i not in [7, 8, 9]):  
            try:
                # Run inference using the model
                total, kategori_terbaik = model.inference(sub_aspek_data)

                # Display the results
                st.subheader("Prediction Results")
                st.write(f"Total Score: {total}")
                st.write(f"Recommended Placement Category: {kategori_terbaik}")
            
            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.error("Please fill in all the input fields before submitting. All values must be provided and greater than 0, except for A8, A9, and A10.")

if __name__ == "__main__":
    show()
