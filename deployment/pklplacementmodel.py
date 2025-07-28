import pandas as pd

class PKLPlacementModel:
    def __init__(self):
        self.sub_aspek_mapping = self.map_sub_aspek_to_kode()

    def map_sub_aspek_to_kode(self):
        # Memetakan nama sub-aspek ke A1-A11
        data = [
            ("Informatika", "A1"),
            ("Dasar Program Keahlian", "A2"),
            ("Projek Kreatif dan Kewirausahaan", "A3"),
            ("Perencanaan dan Pengalamatan Jaringan", "A4"),
            ("Administrasi Sistem Jaringan", "A5"),
            ("Teknologi Jaringan Kabel dan Nirkabel", "A6"),
            ("Pemasangan dan Konfigurasi Perangkat Jaringan", "A7"),
            ("Samsung Tech Institute", "A8"),
            ("Pemrograman Web", "A9"),
            ("Internet of Things", "A10"),
            ("Jarak", "A11")
        ]
        return {item[0]: item[1] for item in data}

    def map_columns_to_A(self, df):
        """
        Fungsi untuk mengganti nama kolom yang sesuai dengan sub-aspek menjadi A1, A2, ..., A11
        Jika kolom sudah menggunakan A1, A2, ..., A11, maka tidak akan diubah.
        """
        sub_aspek = list(self.sub_aspek_mapping.keys())
        A_columns = list(self.sub_aspek_mapping.values())
        
        # Membuat mapping nama kolom yang sesuai dengan sub-aspek
        column_mapping = {sub_aspek[i]: A_columns[i] for i in range(len(sub_aspek))}
        
        # Ganti nama kolom jika kolom tersebut sesuai dengan sub-aspek
        df.columns = [column_mapping.get(col, col) for col in df.columns]
        return df

    def kisaran_rapot(self, rapot):
        if 95 <= rapot <= 100:
            return 8
        elif 90 <= rapot < 95:
            return 7
        elif 85 <= rapot < 90:
            return 6
        elif 80 <= rapot < 85:
            return 5
        elif 75 <= rapot < 80:
            return 4
        elif 70 <= rapot < 75:
            return 3
        elif 65 <= rapot < 70:
            return 2
        elif 0 <= rapot < 65:
            return 1
        else:
            return 0

    def kisaran_jarak(self, jrk):
        if 0 <= jrk <= 2:
            return 8
        elif 2 < jrk <= 4:
            return 7
        elif 4 < jrk <= 6:
            return 6
        elif 6 < jrk <= 8:
            return 5
        elif 8 < jrk <= 10:
            return 4
        elif 10 < jrk <= 12:
            return 3
        elif 12 < jrk <= 14:
            return 2
        elif jrk > 14:
            return 1
        else:
            return 0

    def konversi(self, sub_aspek):
        konversi_rapot = [self.kisaran_rapot(sub_aspek[i]) for i in range(10)]  
        konversi_jarak = self.kisaran_jarak(sub_aspek[10]) 
        return konversi_rapot + [konversi_jarak]

    def gap(self, bbt):
        bobot_gap = {
            0: 9, 1: 8.5, -1: 8, 2: 7.5, -2: 7, 3: 6.5, -3: 6,
            4: 5.5, -4: 5, 5: 4.5, -5: 4, 6: 3.5, -6: 3,
            7: 2.5, -7: 2, 8: 1.5, -8: 1
        }
        return bobot_gap.get(bbt, 0)

    def selisih(self, sub_aspek, jenis_pkl):
        nilai_siswa = self.konversi(sub_aspek)

        jenis_pkl_tiap_label = {
            "Mobile Engineering": [8, 8, 8, 7, 7, 7, 7, 8, 3, 3, 7],
            "Software Engineering": [8, 8, 8, 7, 7, 7, 7, 3, 8, 3, 7],
            "Internet of Things": [8, 8, 7, 7, 7, 7, 7, 3, 3, 8, 7]
        }

        nilai_gap_standar_pkl = jenis_pkl_tiap_label[jenis_pkl]
        selisih_profil_pkl = [nilai_siswa[i] - nilai_gap_standar_pkl[i] for i in range(len(nilai_siswa))]
        return [self.gap(selisih_gap) for selisih_gap in selisih_profil_pkl]

    def pengurutan_penempatan(self, sub_aspek, jenis_pkl):
        hasil_bobot_gap = self.selisih(sub_aspek, jenis_pkl)

        cf = [hasil_bobot_gap[i] for i in range(7) if i != 2]
        sf = hasil_bobot_gap[7:10] + [hasil_bobot_gap[2]]  
        aspek_cf = sum(cf) / len(cf) 
        aspek_sf = sum(sf) / len(sf)
        total_aspek_1 = (aspek_cf * 0.6) + (aspek_sf * 0.4)

        nfl = hasil_bobot_gap[10]  
        total_aspek_2 = nfl 

        return (total_aspek_1 * 0.6) + (total_aspek_2 * 0.4)

    def inference(self, sub_aspek_data):
        nilai_penempatan = {}

        for jenis_pkl in ["Mobile Engineering", "Software Engineering", "Internet of Things"]:
            nilai_penempatan[jenis_pkl] = self.pengurutan_penempatan(sub_aspek_data, jenis_pkl)

        kategori_terbaik = max(nilai_penempatan, key=nilai_penempatan.get)
        total = nilai_penempatan[kategori_terbaik]

        return total, kategori_terbaik
