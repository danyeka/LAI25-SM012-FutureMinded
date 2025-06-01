![](Logo/FM_logo_full.png)
=======

# FutureMinded : Make Your Own Choice
## Team ID: LAI25-SM012
**Team Member :**
|                 Name            | LaskarAI-ID   |      Path     |            University             |
| --------------------------------| --------------| --------------| ----------------------------------|
| Dany Eka Saputra                | A471YBF113    | AI Engineer   | Universitas Teknokrat Indonesia   |
| Zid Irsyadin Sartono Wijaogy    | A208YAF520    | AI Engineer   | Universitas Hasanuddin            |
| T. Muhammad Caesar Maulana      | A322YBF474    | AI Engineer   | Universitas Syiah Kuala           |
| Nurnia Hamid                    | A309XAF385    | AI Engineer   | Universitas Sam Ratulangi         |


## Project Overview
This project is a web-based personality test application implementing the RIASEC theory (Realistic, Investigative, Artistic, Social, Enterprising, Conventional) to help users identify their career interests. The application is built using Streamlit and provides several features such as:

- A personality test with 12 questions
- Radar chart visualization of the results
- Description of the dominant personality type
- Career recommendations based on personality
- Downloadable test results in PDF format

### Application Structure

- The application consists of three main pages: **Start**, **Test**, and **Results**
- Session state is used to store user answers and theme preferences
- Supports dark/light mode toggle

### Test Flow

1. User inputs their name
2. Answers 12 questions on a scale from 0–2 (Disagree, Neutral, Agree)
3. The system calculates scores for each personality type
4. Displays the results using visualizations and recommendations

### Visualization

- Utilizes Matplotlib to generate a radar (hexagon) chart
- Each personality type is assigned a specific color and position on the chart

### PDF Report

- Uses FPDF to generate a personalized test report
- Report includes scores, radar diagram, dominant type description, and job recommendations

---

## Features

- Interactive RIASEC personality test
- Radar chart result visualization
- Personality type interpretation
- Career recommendations
- Export results as PDF
- Dark/Light theme toggle

---

## Technologies Used

- **Python 3.x**
- **Streamlit** – Web framework
- **Pandas, NumPy** – Data processing
- **Matplotlib** – Data visualization
- **FPDF** – PDF generation
- **PIL** – Image processing

---

## Installation

### Prerequisites

- Ensure Python 3.x is installed
- It is recommended to use a virtual environment

### Steps

```bash
# Clone the repository
git clone [REPOSITORY_URL]
cd [FOLDER_NAME]

# Create and activate virtual environment (optional but recommended)
python -m venv venv

# For Windows:
venv\Scripts\activate

# For Unix/MacOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run app.py
```
## Struktur File

```
.
├── app.py                # File utama aplikasi
├── requirements.txt      # Dependencies
├── README.md             # Dokumentasi ini
└── assets/               # Folder untuk aset (logo, dll)
    └── FM_logo_full.png  # Logo aplikasi
```
    
## Reference


