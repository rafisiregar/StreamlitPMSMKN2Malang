import io
import streamlit as st  # type:ignore
import matplotlib.pyplot as plt
import pandas as pd
import xlsxwriter

def show():
    # Title of the Dashboard
    st.title("📊 PKL Placement Dashboard for SMK Negeri 2 Malang")

    # Description: About the Application
    # Section: Purpose of the Dashboard
    st.markdown("""
## 💡 About

This application is designed to help determine the **most appropriate PKL placement** for students based on their academic performance and skills. 
By uploading an Excel file with student data, the app will use a **Profile Matching Algorithm** to provide personalized PKL placement recommendations.

---
                
### 📚 The dashboard was developed to:
- Explore student data from SMK based on their report card results and PKL placements.
- Predict the most suitable PKL placement category for students: **Mobile Engineering**, **Software Engineering**, or **Internet of Things**.
- Present visualizations of the modeling performance and PKL placement selection process.

---
                
## 🗺️ How It Works:
1. **Upload Your Data**: Simply drag and drop an Excel file with student data in the required format.
2. **Data Review**: After uploading, you will see a preview of the data, including student names, their grades across various subjects (A1-A11), and their class (`Kelas`).
3. **Prediction**: Once the data is uploaded, click on the **"🔍 Predict!"** button to receive the **recommended PKL placement** for each student, based on their academic performance.
4. **Download Results**: You can download the results in an **Excel file**, which will include the recommended PKL category for each student along with their total score.

---

### 🎨 What do A1 to A11 represent?
These represent the **different subjects/competencies** that will be evaluated for each student. Here's what each code stands for:
| **Subject**                                   | **Code** | **Description**                               |
| --------------------------------------------- | -------- | --------------------------------------------- |
| Informatika                                   | A1       | Informatics (Computer Science)                |
| Dasar Program Keahlian                        | A2       | Basic Program Expertise                       |
| Projek Kreatif dan Kewirausahaan              | A3       | Creative Projects and Entrepreneurship        |
| Perencanaan dan Pengalamatan Jaringan         | A4       | Network Planning and Addressing               |
| Administrasi Sistem Jaringan                  | A5       | Network System Administration                 |
| Teknologi Jaringan Kabel dan Nirkabel         | A6       | Cable and Wireless Network Technologies       |
| Pemasangan dan Konfigurasi Perangkat Jaringan | A7       | Network Device Installation and Configuration |
| Samsung Tech Institute                        | A8       | Samsung Tech Certification                    |
| Pemrograman Web                               | A9       | Web Programming                               |
| Internet of Things                            | A10      | IoT Technologies                              |
| Jarak                                         | A11      | Distance (specific to program)                |

Once your data is uploaded, the algorithm will use this information to predict the best PKL category for each student based on their performance in these subjects.
                
---
""")
    


    # Section: Dataset and Distribution
    st.markdown("""
### 📁 Dataset Requirements
            
    
This model is trained using a dataset that includes student data from SMK, covering their report card results and types of PKL placements.

**Important**: Please ensure that the dataset you upload meets the following requirements, as it is crucial for accurate PKL placement predictions. You can download the dataset template below to help guide your data formatting.

**Original Dataset** comes from internal processing, including the following data:
  - **Student report card results** across various fields of study.
  - **PKL placements** across categories such as *Mobile Engineering*, *Software Engineering*, and *Internet of Things*.

**Here are the example data requirements for predicting PKL Placement:**

- The dataset should include student names, grades for each subject (A1 to A11), and their major (Jurusan).
- Data should be in tabular format, as shown in the example below.

🚨 **Attention**: The dataset **must** be in **.xlsx** format for proper processing! Please make sure to upload an **Excel file (.xlsx)** and **NOT** a CSV or any other file type! 🚨

If you need the template to ensure your data is properly formatted, you can download it by clicking the button below.
""")
    
    # Create and display dummy dataset
    # Define the dataset
    data = {
        "NIS": [17045, 17046, 17047, 17048, 17049],
        "Full Name": [
            "MUHAMMAD HANS ADICANDRA KU",
            "MUHAMMAD YUSUF ALFARIZQI",
            "PUTRI ANGGITA NUR HASANAH",
            "RADITIYA ILHAM PUTRA",
            "RAFA GASTIADIRRIJAL FAWAS"
        ],
        "A1": [79.5, 74.5, 77.5, 83, 75.5],
        "A2": [84, 80.5, 86.5, 92.5, 81.5],
        "A3": [85.5, 80.5, 88, 94.5, 84.5],
        "A4": [75.5, 83, 87.5, 88, 78.5],
        "A5": [80.5, 82.5, 85.5, 88, 84.5],
        "A6": [88.5, 82.5, 88.5, 89, 90.5],
        "A7": [85, 82.5, 89.5, 79.5, 81],
        "A8": [76, 84, 79.5, 81.5, 80],
        "A9": [88, 75, 90, 85, 80],  # Added values for Web Programming (A9)
        "A10": [92, 80, 85, 90, 82],  # Added values for Internet of Things (A10)
        "A11": [4.4, 3, 2.5, 7.7, 3.9],
        "Class": ["TKJ 1", "TKJ 2", "TKJ 3", "TKJ 1", "TKJ 2"]
    }

    # Create DataFrame
    df = pd.DataFrame(data)
    st.dataframe(df)

    # Convert the DataFrame to an Excel file
    excel_file = io.BytesIO()
    with pd.ExcelWriter(excel_file, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="Student Data")
    excel_file.seek(0)

    # Provide a download button for the Excel file
    st.download_button(
        label="Download Dataset as Excel",
        data=excel_file,
        file_name="student_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.markdown("---")

    # Section: How to Use the Application
    st.markdown("""
### 🛠️ How to Use the Application

- Use the left sidebar for navigation:
  - 🔍 **Home**
  - 📚 **PKL Placement Prediction**
  - 🤖 **Try On!**

- Upload student report card data in **.xlsx** format to make PKL placement predictions.
- The model will process the report card data and display the most suitable PKL placement prediction along with the confidence level.

- These predictions are useful for recommending the best PKL placement based on the available analysis and the model.

---

Good luck and we hope this application proves helpful in guiding the PKL placement for SMK students! 🚀🎓
""")

if __name__ == "__main__":
    show()
