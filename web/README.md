# Tes Kepribadian RIASEC - FutureMinded

## Deskripsi Proyek

Aplikasi ini adalah tes kepribadian berbasis web yang mengimplementasikan teori RIASEC (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) untuk membantu pengguna menemukan minat karir mereka. Aplikasi dibangun menggunakan Streamlit dan menyediakan fitur:

- Tes kepribadian dengan 12 pertanyaan
- Visualisasi hasil dalam bentuk diagram radar
- Deskripsi tipe kepribadian dominan
- Rekomendasi pekerjaan yang sesuai
- Laporan hasil dalam format PDF

## Cara Kerja

### Struktur Aplikasi

- Terdiri dari 3 halaman utama: **Start**, **Test**, dan **Results**
- Menggunakan session state untuk menyimpan jawaban pengguna dan preferensi tema
- Mendukung dark/light mode toggle

### Alur Tes

1. Pengguna memasukkan nama
2. Menjawab 12 pertanyaan dengan skala 0-2 (Tidak Setuju, Netral, Setuju)
3. Sistem menghitung skor untuk setiap tipe kepribadian
4. Menampilkan hasil dengan visualisasi dan rekomendasi

### Visualisasi

- Menggunakan Matplotlib untuk membuat diagram radar (hexagon)
- Setiap tipe kepribadian memiliki warna dan posisi tertentu dalam diagram

### Laporan PDF

- Menggunakan FPDF untuk menghasilkan laporan hasil tes
- Laporan mencakup skor, diagram, deskripsi tipe dominan, dan rekomendasi pekerjaan

## Teknologi yang Digunakan

- Python 3.x
- Streamlit (framework web)
- Pandas, NumPy (pengolahan data)
- Matplotlib (visualisasi)
- FPDF (generasi PDF)
- PIL (image processing)

## Panduan Instalasi

### Prasyarat

- Pastikan Python 3.x sudah terpasang di sistem Anda
- Disarankan menggunakan virtual environment

### Langkah-langkah

1. Clone repositori ini:
    ```bash
    git clone [URL_REPOSITORI]
    cd [NAMA_FOLDER]
    ```
2. Buat dan aktifkan virtual environment (opsional tapi disarankan):
    ```bash
    python -m venv venv
    # Untuk Windows:
    venv\Scripts\activate
    # Untuk Unix/MacOS:
    source venv/bin/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Jalankan aplikasi:
    ```bash
    streamlit run app.py
    ```
5. Aplikasi akan berjalan di browser default Anda pada:  
   [http://localhost:8501](http://localhost:8501)

## Cara Penggunaan

1. Masukkan nama Anda di halaman awal
2. Klik **"Mulai Tes"**
3. Jawab semua pertanyaan dengan jujur
4. Lihat hasil tes dan rekomendasi karir
5. Download hasil dalam format PDF jika diperlukan

## Web Demo

Aplikasi dapat diakses secara online di:  
[https://futureminded-riasec.streamlit.app](https://futureminded-riasec.streamlit.app)

## Struktur File

```
.
├── app.py                # File utama aplikasi
├── requirements.txt      # Dependencies
├── README.md             # Dokumentasi ini
└── assets/               # Folder untuk aset (logo, dll)
    └── FM_logo_full.png  # Logo aplikasi
```

## Lisensi

Proyek ini dilisensikan di bawah MIT License. Lihat file LICENSE untuk detail lebih lanjut.
