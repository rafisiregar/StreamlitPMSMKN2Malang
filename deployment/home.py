import streamlit as st # type:ignore
import matplotlib.pyplot as plt

def show():
    st.title("📊 Dashboard Penempatan PKL SMK Negeri 2 Malang")

    st.markdown("""
### 🎯 Tujuan Dashboard

Dashboard ini dikembangkan untuk:
- Mengeksplorasi data siswa SMK berdasarkan hasil rapot dan penempatan PKL.
- Memprediksi kategori penempatan PKL yang paling sesuai untuk siswa: **Mobile Engineering**, **Software Engineering**, atau **Internet of Things**.
- Menyajikan visualisasi performa pemodelan dan proses seleksi penempatan PKL.

---

### 💡 Latar Belakang Studi Kasus

Saya adalah seorang **data scientist** di sebuah lembaga pendidikan di Jakarta. Seiring dengan meningkatnya kebutuhan akan penempatan PKL yang lebih **personalisasi** dan berbasis data, tim kami berinisiatif mengembangkan teknologi berbasis *machine learning* untuk membantu penentuan penempatan PKL siswa SMK secara otomatis.

---

### 🧠 Arsitektur Model

Model yang digunakan berbasis **ResNet50** pretrained yang digunakan sebagai feature extractor dengan beberapa lapisan tambahan seperti **Dense**, **Dropout**, dan **BatchNormalization** untuk klasifikasi penempatan PKL. Model ini dilatih untuk memprediksi penempatan siswa ke 3 kategori: **Mobile Engineering**, **Software Engineering**, dan **Internet of Things**.

Optimisasi menggunakan **SGD** (learning rate 0.001, momentum 0.9), dan **EarlyStopping** untuk mencegah overfitting.

**Hasil Evaluasi:**
-  Akurasi Data Train: **35.8%**
-  Akurasi Data Testing: **34.3%**
-  Model terkadang mengalami kesulitan dalam mengklasifikasikan penempatan yang tepat untuk beberapa siswa
-  Skor f1 untuk kategori *Mobile Engineering* dan *Software Engineering* masih rendah

> Kesimpulan: Model menunjukkan potensi yang baik tetapi masih memerlukan penyempurnaan lebih lanjut untuk meningkatkan kualitas prediksi, terutama pada data yang lebih beragam.

---

### 📁 Dataset yang Digunakan

Model ini dilatih menggunakan dataset yang mencakup data siswa SMK, termasuk hasil rapot dan jenis penempatan PKL.

- **Dataset Asli** berasal dari hasil pengolahan internal yang mencakup data berikut:
  - **Hasil rapot siswa** dari berbagai bidang keahlian
  - **Penempatan PKL** di beberapa kategori seperti *Mobile Engineering*, *Software Engineering*, dan *Internet of Things*

**Distribusi Penempatan PKL pada Data:**
""")

    # Tampilkan pie chart
    labels = ['Mobile Engineering (120)', 'Software Engineering (150)', 'Internet of Things (100)']
    sizes = [120, 150, 100]
    colors = ['#8ecae6', '#ffb703', '#fb8500']

    fig, ax = plt.subplots(figsize=(3.5, 3.5))
    ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    st.pyplot(fig)

    st.markdown("---")

    st.markdown("""
### 🛠️ Petunjuk Penggunaan Aplikasi

- Gunakan sidebar di sebelah kiri untuk navigasi:
  - 🔍 Home
  - 📊 Explanatory Data Analysis
  - 📚 Prediksi Penempatan PKL

- Unggah data rapot siswa dalam format **.csv** untuk melakukan prediksi penempatan PKL
- Model akan memproses data rapot dan menampilkan hasil prediksi penempatan PKL yang paling sesuai, beserta tingkat kepercayaannya.

- Hasil prediksi ini berguna untuk memberikan rekomendasi penempatan PKL terbaik berdasarkan hasil analisis dan model yang ada.

---

Selamat mencoba dan semoga aplikasi ini bermanfaat untuk membantu penempatan PKL siswa SMK! 🚀🎓
""")
