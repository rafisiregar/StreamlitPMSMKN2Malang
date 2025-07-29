# 📊 PKL Placement Dashboard for SMK Negeri 2 Malang

This project is to analyze and developed web-based application is designed to assist in determining the **most suitable PKL (Praktek Kerja Lapangan or Field Work Practice)** placements for students at **SMK Negeri 2 Malang**. The application uses a **Profile Matching Algorithm** to generate personalized PKL placement recommendations based on students' academic performance and skills. It incorporates **data analysis** to ensure accurate predictions and employs **Streamlit** for easy deployment and interaction.

---

## 🚀 Features

- **Data Upload**: Upload a student dataset in `.csv` format that contains report card data (A1-A11) and student major information.
- **Personalized PKL Placement**: After uploading the dataset, the application will predict the best PKL placement for each student based on their academic performance.
- **Downloadable Results**: Once predictions are made, you can download the results in an Excel format, which includes the recommended PKL category for each student and their total scores.
- **Dataset Preview**: The application provides a preview of the data you upload to ensure it’s in the correct format.
- **Data Visualization**: The app includes an interactive pie chart that visualizes the distribution of PKL placements (Mobile Engineering, Software Engineering, IoT).

---

## 📊 How it Works

### Steps:

1. **Upload Data**: Drag and drop an Excel file containing student data in the required format (with columns for student names, grades, and major).
2. **View Data**: The app will display the uploaded data for you to review, including subjects (A1-A11) and major information.
3. **Predict PKL Placement**: Click the **🔍 Prediksi!** button to generate the best possible PKL placement for each student based on their academic performance.
4. **Download Results**: After predictions are generated, you can download the results in an **Excel file**, which will include:
   - The best PKL category for each student (Mobile Engineering, Software Engineering, IoT)
   - Total scores for students

---

## 📁 Dataset Requirements

To ensure accurate predictions, the dataset should follow these guidelines:

- The dataset must include the following columns:
  - **NIS (Student ID)**: Unique student identifier
  - **Full Name**: Name of the student
  - **A1-A11**: Grades for various subjects (e.g., A1 for Informatics, A2 for Basic Program Expertise)
  - **Major (Jurusan)**: Student's major (e.g., "TKJ 1", "TKJ 2")

A dataset template can be downloaded directly from the app to help guide the formatting of your data.

---

## 📈 Example Data

Here is an example dataset used to predict PKL placements:

| **NIS** | **Full Name**        | **A1** | **A2** | **A3** | **A4** | **A5** | **A6** | **A7** | **A8** | **A9** | **A10** | **A11** | **Major** |
| ------------- | -------------------------- | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------- | ------------- | --------------- |
| 17045         | MUHAMMAD HANS ADICANDRA KU | 79.5         | 84           | 85.5         | 75.5         | 80.5         | 88.5         | 85           | 76           | 88           | 92            | 4.4           | TKJ 1           |
| 17046         | MUHAMMAD YUSUF ALFARIZQI   | 74.5         | 80.5         | 80.5         | 83           | 82.5         | 82.5         | 82.5         | 84           | 75           | 80            | 3             | TKJ 2           |
| 17047         | PUTRI ANGGITA NUR HASANAH  | 77.5         | 86.5         | 88           | 87.5         | 85.5         | 88.5         | 89.5         | 79.5         | 90           | 85            | 2.5           | TKJ 3           |

---

## 📥 Download Data

Once you upload your student data, the application will process it and allow you to **download the results as an Excel file**, including the best PKL categories for each student.

---

## ⚙️ Technologies Used

This application uses the following technologies:

- **Streamlit**: For creating the interactive web-based user interface.
- **Pandas**: For data manipulation and analysis, including importing, cleaning, and processing student data.
- **Matplotlib**: For visualizing the distribution of PKL placements via interactive charts.
- **XlsxWriter**: For exporting the data and results to downloadable Excel files.

---

## 🛠️ How to Run Locally

If you'd like to run the application on your local machine:

1. Clone this repository or download the code.
2. Install the required dependencies using pip:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```
4. The app will be accessible locally via the URL provided by Streamlit, where you can interact with it.

---

## 🔗 Link to App

You can access the live version of the application here: [PKL Placement Dashboard](https://penempatanpklsmkn2malang.streamlit.app/)
