import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch
from fpdf import FPDF
import base64
from datetime import datetime
import tempfile
import os
from PIL import Image

# Data pertanyaan RIASEC
questions = [
    {"question": "Saya suka bekerja dengan alat-alat atau mesin.", "type": "R"},
    {"question": "Saya senang membantu orang lain dengan masalah mereka.", "type": "S"},
    {"question": "Saya suka bekerja dengan angka dan data.", "type": "C"},
    {"question": "Saya menikmati kegiatan kreatif seperti melukis atau menulis.", "type": "A"},
    {"question": "Saya suka memimpin dan mempengaruhi orang lain.", "type": "E"},
    {"question": "Saya tertarik mempelajari tumbuhan dan hewan.", "type": "I"},
    {"question": "Saya senang memperbaiki barang-barang elektronik.", "type": "R"},
    {"question": "Saya suka mengajar atau melatih orang lain.", "type": "S"},
    {"question": "Saya teliti dalam mengatur dokumen dan arsip.", "type": "C"},
    {"question": "Saya memiliki imajinasi yang kuat.", "type": "A"},
    {"question": "Saya pandai meyakinkan orang lain.", "type": "E"},
    {"question": "Saya senang melakukan eksperimen ilmiah.", "type": "I"},
]

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

def create_riasec_chart(scores, dark_mode=False):
    # Urutan tipe sesuai diagram RIASEC (hexagon)
    types = ['R', 'I', 'A', 'S', 'E', 'C']
    labels = [riasec_types[t]['name'] for t in types]
    colors = [riasec_types[t]['color'] for t in types]
    values = [scores[t] for t in types]
    
    # Normalisasi nilai ke 0-100
    normalized_values = [v for v in values]
    
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
    
    # Atur grid
    ax.set_rlabel_position(0)
    plt.yticks([20, 40, 60, 80, 100], ["20", "40", "60", "80", "100"], 
               color="white" if dark_mode else "black", size=8)
    plt.ylim(0, 100)
    
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
        pdf.cell(0, 10, f"{riasec_types[type_code]['name']}: {score}%", 0, 1)
    
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
    
    # Halaman hasil
    elif st.session_state.page == "results":
        render_results_page()

def render_start_page():
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.image("../Logo/FM_logo_full.png")
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
    st.markdown(f"<p style='color: var(--text);'>Silakan jawab pertanyaan berikut dengan sejujurnya:</p>", unsafe_allow_html=True)
    
    # Tampilkan progress bar
    progress = len(st.session_state.answers) / len(questions)
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress * 100}%;"></div>
    </div>
    <p style="text-align: center; color: var(--text);">Pertanyaan {len(st.session_state.answers) + 1} dari {len(questions)}</p>
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
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Tidak Setuju", key=f"no_{current_index}"):
                st.session_state.answers[current_index] = 0
                st.rerun()
        with col2:
            if st.button("Netral", key=f"neutral_{current_index}"):
                st.session_state.answers[current_index] = 1
                st.rerun()
        with col3:
            if st.button("Setuju", key=f"yes_{current_index}"):
                st.session_state.answers[current_index] = 2
                st.rerun()
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
    
    # Normalisasi skor (0-100)
    for k in scores:
        question_count = len([q for q in questions if q["type"] == k])
        if question_count > 0:
            scores[k] = int((scores[k] / (2 * question_count)) * 100)
    
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
                <h3>{score}%</h3>
            </div>
            """, unsafe_allow_html=True)
    
    # Tampilkan diagram RIASEC
    st.markdown("<h3 style='color: var(--text);'>Profil Kepribadian:</h3>", unsafe_allow_html=True)
    chart_path = create_riasec_chart(scores, st.session_state.dark_mode)
    # Center the chart using Streamlit columns
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
    
    # Rekomendasi pekerjaan
    recommended_jobs = {
        "R": ["Teknisi Mesin", "Insinyur Sipil", "Montir", "Pilot", "Arsitek Lansekap"],
        "I": ["Ilmuwan", "Dokter", "Apoteker", "Psikolog", "Peneliti"],
        "A": ["Desainer Grafis", "Penulis", "Musisi", "Aktor", "Fotografer"],
        "S": ["Guru", "Perawat", "Konselor", "Pekerja Sosial", "Psikolog Klinis"],
        "E": ["Pengusaha", "Manajer", "Sales", "Pengacara", "Marketing Manager"],
        "C": ["Akuntan", "Sekretaris Eksekutif", "Analis Data", "Pustakawan", "Auditor"]
    }
    
    st.markdown(f"""
    <div class="result-card">
        <h3 style='color: var(--text);'>Rekomendasi Pekerjaan:</h3>
        {''.join([f"<p style='color: var(--text);'>✅ {job}</p>" for job in recommended_jobs[dominant_type]])}
    </div>
    """, unsafe_allow_html=True)
    
    # Buat dan tampilkan tombol download PDF
    pdf_output = create_pdf(
        st.session_state.name, 
        scores, 
        dominant_type, 
        recommended_jobs[dominant_type],
        chart_path
    )
    st.markdown(get_pdf_download_link(pdf_output, st.session_state.name), unsafe_allow_html=True)

if __name__ == "__main__":
    main()