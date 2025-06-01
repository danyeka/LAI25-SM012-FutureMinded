import os
import time
import base64
import joblib
import tempfile
import numpy as np
import pandas as pd
from fpdf import FPDF
from PIL import Image
import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from tensorflow.keras.models import load_model

# # Load model dan scaler
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
riasec_types_list = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']\

# Data pertanyaan RIASEC yang diperbarui
questions = [
    {"question": "Saya suka bekerja dengan alat, mesin, atau tanaman.", "type": "R"},
    {"question": "Saya senang menyelidiki masalah atau memecahkan teka-teki.", "type": "I"},
    {"question": "Saya suka menggambar, melukis, atau menulis cerita.", "type": "A"},
    {"question": "Saya menikmati membantu orang menyelesaikan masalah.", "type": "S"},
    {"question": "Saya suka memimpin proyek atau orang.", "type": "E"},
    {"question": "Saya menikmati bekerja dengan data atau angka.", "type": "C"},
    {"question": "Saya menikmati aktivitas fisik atau pekerjaan lapangan.", "type": "R"},
    {"question": "Saya suka menganalisis informasi dan melakukan eksperimen.", "type": "I"},
    {"question": "Saya suka tampil di depan umum seperti berakting atau menyanyi.", "type": "A"},
    {"question": "Saya senang mengajar atau melatih orang lain.", "type": "S"},
    {"question": "Saya suka menjual atau mempromosikan ide atau produk.", "type": "E"},
    {"question": "Saya suka pekerjaan yang melibatkan rutinitas dan struktur.", "type": "C"},
    {"question": "Saya suka menggunakan alat atau kendaraan.", "type": "R"},
    {"question": "Saya penasaran dengan bagaimana sesuatu bekerja.", "type": "I"},
    {"question": "Saya suka mendesain atau membuat hal kreatif.", "type": "A"},
    {"question": "Saya suka mendengarkan masalah orang dan membantu mereka.", "type": "S"},
    {"question": "Saya suka mengambil keputusan dan mengambil risiko.", "type": "E"},
    {"question": "Saya suka mengatur data atau menyusun informasi.", "type": "C"},
    {"question": "Saya suka membangun atau memperbaiki sesuatu.", "type": "R"},
    {"question": "Saya suka memecahkan masalah menggunakan logika.", "type": "I"},
    {"question": "Saya suka menulis puisi, cerita, atau lagu.", "type": "A"},
    {"question": "Saya suka menjadi sukarelawan dalam kegiatan sosial.", "type": "S"},
    {"question": "Saya suka menjadi pemimpin dalam kelompok.", "type": "E"},
    {"question": "Saya suka bekerja dengan komputer dan angka.", "type": "C"},
    {"question": "Saya senang menggunakan kekuatan atau ketangkasan saya.", "type": "R"},
    {"question": "Saya suka bertanya dan mengeksplorasi hal baru.", "type": "I"},
    {"question": "Saya suka membuat karya seni atau musik.", "type": "A"},
    {"question": "Saya suka mendengarkan dan memberi nasihat.", "type": "S"},
    {"question": "Saya suka mengatur orang untuk mencapai tujuan.", "type": "E"},
    {"question": "Saya suka bekerja dengan detail dan mengikuti instruksi.", "type": "C"},
    {"question": "Saya suka bekerja di luar ruangan.", "type": "R"},
    {"question": "Saya suka meneliti dan menganalisis masalah.", "type": "I"},
    {"question": "Saya suka mengekspresikan diri melalui seni atau drama.", "type": "A"},
    {"question": "Saya suka membimbing dan mengajar orang.", "type": "S"},
    {"question": "Saya suka meyakinkan orang lain untuk membeli sesuatu.", "type": "E"},
    {"question": "Saya suka menyusun laporan atau membuat tabel data.", "type": "C"},
    {"question": "Saya suka menggunakan peralatan atau instrumen.", "type": "R"},
    {"question": "Saya suka memecahkan teka-teki logika.", "type": "I"},
    {"question": "Saya suka bermain musik atau menari.", "type": "A"},
    {"question": "Saya suka membantu orang mengembangkan diri.", "type": "S"},
    {"question": "Saya suka menjadi pemimpin proyek.", "type": "E"},
    {"question": "Saya suka pekerjaan administratif atau perkantoran.", "type": "C"}
]

# Indeks pertanyaan untuk setiap tipe RIASEC
riasec_index = {
    'R': [0, 6, 12, 18, 24, 30, 36],
    'I': [1, 7, 13, 19, 25, 31, 37],
    'A': [2, 8, 14, 20, 26, 32, 38],
    'S': [3, 9, 15, 21, 27, 33, 39],
    'E': [4, 10, 16, 22, 28, 34, 40],
    'C': [5, 11, 17, 23, 29, 35, 41]
}

# Deskripsi tipe kepribadian RIASEC
riasec_types = {
    "R": {
        "name": "Realistic",
        "description": "Orang dengan tipe Realistik menyukai kegiatan praktis, bekerja dengan tangan, alat, mesin, atau binatang.",
        "color": "#FF6B6B"  # Merah
    },
    "I": {
        "name": "Investigative",
        "description": "Orang dengan tipe Investigatif menyukai kegiatan yang melibatkan pemikiran, pengamatan, dan pemecahan masalah.",
        "color": "#4ECDC4"  # Cyan
    },
    "A": {
        "name": "Artistic",
        "description": "Orang dengan tipe Artistik menyukai kegiatan yang tidak terstruktur dan kreatif seperti seni, musik, atau menulis.",
        "color": "#FFBE0B"  # Kuning
    },
    "S": {
        "name": "Social",
        "description": "Orang dengan tipe Sosial menikmati membantu, mengajar, atau melayani orang lain.",
        "color": "#A5DD9B"  # Hijau
    },
    "E": {
        "name": "Enterprising",
        "description": "Orang dengan tipe Enterprising menyukai kegiatan memimpin, mempengaruhi orang lain, dan bisnis.",
        "color": "#FF9F1C"  # Oranye
    },
    "C": {
        "name": "Conventional",
        "description": "Orang dengan tipe Konvensional menyukai pekerjaan terstruktur yang melibatkan data dan detail.",
        "color": "#A78AFF"  # Ungu
    }
}

# Warna tema
light_mode = {
    "primary": "#6C5CE7",
    "secondary": "#A29BFE",
    "background": "#FFFFFF",
    "card": "#F8F9FA",
    "text": "#2D3436",
    "text_secondary": "#636E72",
    "border": "#DFE6E9",
    "input_background": "#F0F2F6",
    "input_text": "#2D3436",
    "input_border": "none"
}

dark_mode = {
    "primary": "#A78AFF",
    "secondary": "#6C5CE7",
    "background": "#121212",
    "card": "#1E1E1E",
    "text": "#FFFFFF",
    "text_secondary": "#B2B2B2",
    "border": "#424242",
    "input_background": "#2D2D2D",
    "input_text": "#FFFFFF",
    "input_border": "none"
}

def recommend_jobs(user_scores, top_n=5):
    user_df = pd.DataFrame([user_scores], columns=riasec_types_list)
    scaled = st.session_state.scaler.transform(user_df)
    user_embed = st.session_state.model.predict(scaled)
    job_embed = st.session_state.model.predict(st.session_state.scaler.transform(st.session_state.df_pivot[riasec_types_list].values))

    # cosine similarity
    user_norm = np.linalg.norm(user_embed, axis=1, keepdims=True)
    job_norm = np.linalg.norm(job_embed, axis=1, keepdims=True)
    sim = np.dot(job_embed, user_embed.T) / (job_norm * user_norm.T + 1e-8)
    sim = sim.flatten()
    
    top_idx = sim.argsort()[-top_n:][::-1]
    result = st.session_state.df_pivot.iloc[top_idx][['Title', 'Job Family']].copy()
    result['Similarity Score'] = sim[top_idx]
    result['Similarity Score'] = result['Similarity Score'].round(3)
    top_dim = user_df.iloc[0].sort_values(ascending=False).head(2).index.tolist()
    result['Alasan'] = f"Skor tertinggi Anda pada dimensi {top_dim[0]} dan {top_dim[1]}"
    return result.reset_index(drop=True)

def create_riasec_chart(scores, dark_mode=False):
    # Urutan tipe sesuai diagram RIASEC (hexagon)
    types = ['R', 'I', 'A', 'S', 'E', 'C']
    labels = [riasec_types[t]['name'] for t in types]
    colors = [riasec_types[t]['color'] for t in types]
    values = [scores[t] for t in types]
    
    # Sudut untuk setiap titik dalam hexagon
    angles = np.linspace(0, 2*np.pi, len(types), endpoint=False).tolist()
    angles += angles[:1]  # Tutup loop
    
    # Buat plot
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    fig.patch.set_facecolor('#121212' if dark_mode else '#FFFFFF')
    ax.set_facecolor('#121212' if dark_mode else '#FFFFFF')
    
    # Plot data
    values += values[:1]  # Tutup loop
    ax.fill(angles, values, color=riasec_types[types[0]]['color'], alpha=0.25)
    ax.plot(angles, values, color='white' if dark_mode else 'black', linewidth=2)
    
    # Atur label
    ax.set_theta_offset(np.pi/2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), labels)
    
    # Atur grid untuk skala 1-5
    ax.set_rlabel_position(0)
    plt.yticks([1, 2, 3, 4, 5], ["1", "2", "3", "4", "5"], 
               color="white" if dark_mode else "black", size=8)
    plt.ylim(1, 5)
    
    # Atur warna teks
    for label in ax.get_xticklabels():
        label.set_color("white" if dark_mode else "black")
    
    # Atur grid
    ax.grid(color="white" if dark_mode else "black", alpha=0.1)
    
    # Simpan ke file sementara
    temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(temp_file.name, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    
    return temp_file.name

def set_page_style(dark):
    theme = dark_mode if dark else light_mode
    
    st.markdown(f"""
    <style>
        :root {{
            --primary: {theme['primary']};
            --secondary: {theme['secondary']};
            --background: {theme['background']};
            --card: {theme['card']};
            --text: {theme['text']};
            --text-secondary: {theme['text_secondary']};
            --border: {theme['border']};
            --input-background: {theme['input_background']};
            --input-text: {theme['input_text']};
            --input-border: {theme['input_border']};
        }}
        
        .stApp {{
            background-color: var(--background);
            color: var(--text);
        }}
        
        /* Menghilangkan header Streamlit */
        header {{
            visibility: hidden;
        }}

        /* Hilangkan underline pada link di dalam button dan download-link */
        .stButton a, .stButton a:visited, .stButton a:hover, .stButton a:active,
        .download-link, .download-link:visited, .download-link:hover, .download-link:active {{
            text-decoration: none !important;
            box-shadow: none !important;
        }}
        .css-1d391kg {{
            padding-top: 1rem;
        }}
        
        .stButton>button {{
            border: 2px solid var(--primary);
            color: white;
            background-color: var(--primary);
            border-radius: 10px;
            padding: 0.5rem 1rem;
            transition: all 0.3s;
        }}
        
        .stButton>button:hover {{
            background-color: var(--card);
            color: var(--primary);
            border: 2px solid var(--primary);
        }}
        
        .question-card {{
            background-color: var(--card);
            border-radius: 15px;
            padding: 2rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }}
        
        .answer-btn {{
            margin: 0.5rem;
            width: 100%;
        }}
        
        .result-card {{
            background-color: var(--card);
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }}
        
        .progress-bar {{
            height: 10px;
            background-color: var(--border);
            border-radius: 5px;
            margin-bottom: 1.5rem;
        }}
        
        .progress-fill {{
            height: 100%;
            border-radius: 5px;
            background-color: var(--primary);
            transition: width 0.5s;
        }}
        
        .mode-toggle {{
            position: fixed;
            top: 10px;
            right: 10px;
            z-index: 999;
        }}
        
        /* Styling untuk text input */
        .stTextInput>div>div>input {{
            background-color: var(--input-background) !important;
            color: var(--input-text) !important;
            border: var(--input-border) !important;
            border-radius: 10px !important;
            padding: 0.5rem 1rem !important;
        }}
        
        /* Chart styling */
        .st-bd {{
            background-color: var(--card) !important;
            border: 1px solid var(--border) !important;
            border-radius: 15px !important;
        }}
        
        /* Text colors */
        h1, h2, h3, h4, h5, h6, p, label, .stMarkdown {{
            color: var(--text) !important;
        }}
        
        /* Download link styling */
        .download-link, .download-link:visited, .download-link:hover, .download-link:active {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background-color: var(--primary);
            color: white !important;
            border-radius: 10px;
            text-decoration: none !important;
            transition: all 0.3s;
            border: 2px solid var(--primary);
        }}
        
        .download-link:hover {{
            background-color: var(--card);
            color: var(--primary) !important;
            border: 2px solid var(--primary);
        }}
        
        /* Home button styling */
        .home-button {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 999;
        }}
    </style>
    """, unsafe_allow_html=True)

def create_pdf(name, scores, dominant_type, recommended_jobs, chart_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Add logo if available
    logo_path = os.path.join(BASE_DIR, "../Logo/FM_logo_full.png")
    if os.path.exists(logo_path):
        pdf.image(logo_path, x=10, y=8, w=40)
    
    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Hasil Tes Kepribadian RIASEC", 0, 1, 'C')
    pdf.ln(5)
    
    # Informasi Peserta
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, f"Nama: {name}", 0, 1)
    pdf.cell(0, 10, f"Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
    pdf.ln(10)
    
    # Skor
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Skor Anda:", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    for type_code, score in scores.items():
        pdf.cell(0, 10, f"{riasec_types[type_code]['name']}: {score}", 0, 1)
    
    pdf.ln(10)
    
    # Diagram RIASEC
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Profil Kepribadian:", 0, 1)
    pdf.ln(5)
    # Atur lebar mengikuti rasio gambar agar tidak stretch, tinggi tetap 120
    img = Image.open(chart_path)
    width, height = img.size
    aspect_ratio = width / height
    new_height = 120
    new_width = int(aspect_ratio * new_height)
    pdf.image(chart_path, x=(210 - new_width) // 2, w=new_width, h=new_height)
    pdf.ln(10)
    img.close()  # Pastikan file ditutup sebelum dihapus
    
    # Tipe Dominan
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, f"Tipe Dominan: {riasec_types[dominant_type]['name']}", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, riasec_types[dominant_type]['description'])
    pdf.ln(10)
    
    # Rekomendasi Pekerjaan
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Rekomendasi Pekerjaan:", 0, 1)
    pdf.ln(5)
    
    pdf.set_font("Arial", '', 12)
    for job in recommended_jobs:
        pdf.cell(0, 10, f"- {job}", 0, 1)
    
    # Hapus file chart sementara
    os.unlink(chart_path)
    
    return pdf.output(dest='S').encode('latin1')

def get_pdf_download_link(pdf_output, name):
    b64 = base64.b64encode(pdf_output).decode()
    current_date = datetime.now().strftime("%Y%m%d")
    filename = f"hasil_tes_riasec_{name}_{current_date}.pdf"
    return f'<a class="download-link" style="text-decoration: none !important;" href="data:application/octet-stream;base64,{b64}" download="{filename}">Download Hasil Tes (PDF)</a>'

def render_mode_toggle():
    # Button toggle mode sederhana
    if st.session_state.dark_mode:
        if st.button("☀️ Light Mode", key="mode_toggle"):
            st.session_state.dark_mode = False
            st.rerun()
    else:
        if st.button("🌙 Dark Mode", key="mode_toggle"):
            st.session_state.dark_mode = True
            st.rerun()

def render_home_button():
    if st.session_state.page != "start":
        if st.button("🏠 Home", key="home_button"):
            st.session_state.page = "start"
            st.session_state.answers = {}
            st.rerun()

def main():
    st.set_page_config(page_title="Tes Kepribadian RIASEC", page_icon="🧑‍💼", layout="wide")
    
    # Inisialisasi session state dengan default dark mode
    if 'page' not in st.session_state:
        st.session_state.page = "start"
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = True  # Default dark mode
    
    # Set style berdasarkan mode
    set_page_style(st.session_state.dark_mode)
    
    # Render home button di kiri atas
    with st.container():
        render_home_button()
    
    # Render mode toggle hanya di halaman start
    if st.session_state.page == "start":
        with st.container():
            render_mode_toggle()
    
    # Halaman awal
    if st.session_state.page == "start":
        render_start_page()
    
    # Halaman tes
    elif st.session_state.page == "test":
        render_test_page()
    
    # Halaman hasil - load model hanya saat diperlukan
    elif st.session_state.page == "results":
        # Load model and scaler only when needed
        if 'model' not in st.session_state:
            try:
                with st.spinner('Memproses hasil tes...'):
                    st.session_state.model = load_model(os.path.join(BASE_DIR, "../model/embedding_model.h5"), compile=False)
                    st.session_state.scaler = joblib.load(os.path.join(BASE_DIR, "../model/scaler.pkl"))
                    st.session_state.df_pivot = pd.read_csv(os.path.join(BASE_DIR, "../dataset/job_with_family.csv"))
            except Exception as e:
                st.error(f"Failed to load resources: {str(e)}")
                st.stop()
        
        render_results_page()

def render_start_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        logo_path = os.path.join(BASE_DIR, "../Logo/FM_logo_full.png")
        st.image(logo_path)
        st.markdown(f"<h1 style='color: var(--primary);'>FutureMinded: Make Your Own Choice</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 18px; color: var(--text);'>FutureMinded merupakan platform pengembangan diri yang membantu Anda menemukan minat dan potensi karir melalui Tes Kepribadian RIASEC. Temukan tipe kepribadian dan rekomendasi karir yang sesuai untuk masa depan Anda.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <style>
            .stTextInput>div>div>input {
                background-color: var(--input-background) !important;
                color: var(--input-text) !important;
                border: var(--input-border) !important;
                border-radius: 10px !important;
                padding: 0.5rem 1rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        st.session_state.name = st.text_input("Masukkan nama Anda:", placeholder="Nama Anda")
        
        if st.button("Mulai Tes", key="start_test"):
            if st.session_state.name.strip() == "":
                st.warning("Silakan masukkan nama Anda terlebih dahulu.")
            else:
                st.session_state.page = "test"
                st.rerun()
def render_test_page():
    st.markdown(f"<h1 style='color: var(--primary);'>Tes Kepribadian RIASEC</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: var(--text);'>Halo, {st.session_state.name}!</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='color: var(--text);'>Silakan jawab pertanyaan berikut dengan skala 1 (Sangat Tidak Setuju) sampai 5 (Sangat Setuju):</p>", unsafe_allow_html=True)
    
    # Tampilkan progress bar
    answered_count = len(st.session_state.answers)
    total_questions = len(questions)
    progress = answered_count / total_questions
    
    # Perbaikan di sini: Gunakan min() untuk memastikan tidak melebihi total pertanyaan
    current_question = min(answered_count + 1, total_questions)
    
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%;"></div>
    </div>
    <p style="text-align: center; color: var(--text);">Pertanyaan {current_question} dari {total_questions}</p>
    """, unsafe_allow_html=True)
    
    # Tampilkan pertanyaan yang belum dijawab
    unanswered = [q for i, q in enumerate(questions) if i not in st.session_state.answers]
    
    if unanswered:
        current_q = unanswered[0]
        current_index = questions.index(current_q)
        
        st.markdown(f"""
        <div class="question-card">
            <h3 style='color: var(--text);'>{current_q['question']}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Show buttons directly in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            if st.button("1", key=f"1_{current_index}"):
                st.session_state.answers[current_index] = 1
                st.rerun()
        with col2:
            if st.button("2", key=f"2_{current_index}"):
                st.session_state.answers[current_index] = 2
                st.rerun()
        with col3:
            if st.button("3", key=f"3_{current_index}"):
                st.session_state.answers[current_index] = 3
                st.rerun()
        with col4:
            if st.button("4", key=f"4_{current_index}"):
                st.session_state.answers[current_index] = 4
                st.rerun()
        with col5:
            if st.button("5", key=f"5_{current_index}"):
                st.session_state.answers[current_index] = 5
                st.rerun()

        # Add explanation below the buttons
        st.markdown("""
        <div style="text-align: center; margin-top: 10px; color: var(--text-secondary);">
            <small>
                1: Sangat Tidak Setuju | 
                2: Tidak Setuju | 
                3: Netral | 
                4: Setuju | 
                5: Sangat Setuju
            </small>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Semua pertanyaan telah dijawab
        st.session_state.page = "results"
        st.rerun()

def render_results_page():
    st.markdown(f"<h1 style='color: var(--primary);'>Hasil Tes Kepribadian RIASEC</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: var(--text);'>Untuk {st.session_state.name}</h3>", unsafe_allow_html=True)
    
    # Hitung skor untuk setiap tipe
    scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
    
    for idx, answer in st.session_state.answers.items():
        q_type = questions[idx]["type"]
        scores[q_type] += answer
    
    # Normalisasi skor (rata-rata per tipe)
    for k in scores:
        question_count = len([q for q in questions if q["type"] == k])
        if question_count > 0:
            scores[k] = round(scores[k] / question_count, 2)
    
    # Konversi ke format yang dibutuhkan untuk rekomendasi
    user_scores = [scores['R'], scores['I'], scores['A'], scores['S'], scores['E'], scores['C']]
    
    # Tampilkan skor
    st.markdown("<h3 style='color: var(--text);'>Skor Anda:</h3>", unsafe_allow_html=True)
    
    cols = st.columns(6)
    for i, (type_code, score) in enumerate(scores.items()):
        with cols[i]:
            st.markdown(f"""
            <div style="background-color: {riasec_types[type_code]['color'] + '30'}; 
                        border-radius: 10px; 
                        padding: 1rem; 
                        text-align: center;
                        border-left: 5px solid {riasec_types[type_code]['color']};
                        color: var(--text);">
                <h4>{riasec_types[type_code]['name']}</h4>
                <h3>{score}</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Tampilkan diagram RIASEC (skala 1-5)
    st.markdown("<h3 style='color: var(--text);'>Profil Kepribadian:</h3>", unsafe_allow_html=True)
    chart_path = create_riasec_chart(scores, st.session_state.dark_mode)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image(chart_path)
    
    # Tampilkan deskripsi tipe dominan
    dominant_type = max(scores.items(), key=lambda x: x[1])[0]
    st.markdown(f"""
    <div class="result-card">
        <h3 style='color: var(--text);'>Tipe Dominan: {riasec_types[dominant_type]['name']}</h3>
        <p style='color: var(--text);'>{riasec_types[dominant_type]['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dapatkan rekomendasi pekerjaan menggunakan model
    recommended_jobs_df = recommend_jobs(user_scores)
    
    # Display the recommendations with proper formatting
    st.markdown("<h3 style='color: var(--text);'>Rekomendasi Karier untuk Anda:</h3>", unsafe_allow_html=True)

    # Create a styled table
    st.markdown("""
    <style>
        .job-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        .job-table th {
            background-color: var(--primary);
            color: white;
            padding: 12px;
            text-align: left;
        }
        .job-table td {
            padding: 10px;
            border-bottom: 1px solid var(--border);
        }
        .job-table tr:nth-child(even) {
            background-color: var(--card);
        }
        .job-table tr:hover {
            background-color: var(--secondary);
            opacity: 0.8;
        }
    </style>
    """, unsafe_allow_html=True)

    # Convert DataFrame to HTML and display
    st.markdown(
        recommended_jobs_df.to_html(classes="job-table", index=False, escape=False),
        unsafe_allow_html=True
    )
    
    # Buat dan tampilkan tombol download PDF
    pdf_output = create_pdf(
        st.session_state.name, 
        scores, 
        dominant_type, 
        recommended_jobs_df['Title'].tolist(),
        chart_path
    )
    st.markdown(get_pdf_download_link(pdf_output, st.session_state.name), unsafe_allow_html=True)

if __name__ == "__main__":
    main()