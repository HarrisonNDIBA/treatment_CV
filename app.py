import streamlit as st
import pandas as pd
from pathlib import Path
import re
from base64 import b64encode
import os

# ---------------------------------------------------
# 🧱 CONFIGURATION DE LA PAGE
# ---------------------------------------------------
st.set_page_config(
    page_title="SNCF RH - Matching des Profils",
    layout="wide",
    page_icon="🚄"
)

# ---------------------------------------------------
# 🎨 STYLE - Palette SNCF verte & bleue + tag vert clair
# ---------------------------------------------------
st.markdown("""
    <style>
        body {
            background-color: #C7DB94 !important;
            color: #1B4079 !important;
        }

        .header-box {
            background-color: #FFFFFF;
            border: 2px solid #8FAD88;
            border-radius: 14px;
            padding: 2rem 1rem;
            box-shadow: 0 3px 10px rgba(27,64,121,0.1);
            text-align: center;
            margin-bottom: 3rem;
            max-width: 850px;
            margin-left: auto;
            margin-right: auto;
        }

        .main-logo img { width: 180px; margin-bottom: 1rem; }

        .main-title {
            font-size: 2.4rem;
            font-weight: 800;
            color: #1B4079;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .subtitle {
            font-size: 1.1rem;
            color: #4D7C8A;
            text-align: center;
            font-style: italic;
            margin-bottom: 0;
        }

        .cv-card {
            background-color: #7F9C96;
            border-radius: 12px;
            padding: 1.6rem;
            margin-bottom: 1.2rem;
            box-shadow: 0 3px 8px rgba(27,64,121,0.15);
            border-left: 6px solid #1B4079;
        }

        .cv-card h3 { color: #FFFFFF; margin-bottom: 0.6rem; }
        .cv-card p { color: #F7F7F7; }

        .word-sheet {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: 0 2px 8px rgba(27,64,121,0.1);
            line-height: 1.7;
            color: #000000;
            margin-top: 0.5rem;
            border-left: 5px solid #8FAD88;
        }

        .cv-section {
            border-bottom: 1px solid #D9D9D9;
            padding: 0.7rem 0;
            display: flex;
            align-items: baseline;
        }

        .cv-section:last-child { border-bottom: none; }

        .cv-section b {
            color: #000000;
            min-width: 160px;
            display: inline-block;
            font-weight: 700;
        }

        [data-testid="stExpander"] {
            background-color: #1B4079 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            margin-top: 0.7rem !important;
        }

        [data-testid="stExpander"] div[role="button"] {
            background-color: #1B4079 !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        [data-testid="stExpander"] svg { color: #FFFFFF !important; }

        div.stButton > button {
            background-color: #1B4079;
            color: #FFFFFF;
            font-weight: 600;
            border: 2px solid #8FAD88;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            margin-top: 1rem;
            box-shadow: 0 3px 6px rgba(0,0,0,0.2);
            transition: all 0.2s ease;
        }

        div.stButton > button:hover {
            background-color: #4D7C8A;
            border: 2px solid #1B4079;
            transform: translateY(-1px);
        }

        .badge-not {
            background-color: #D9D9D9;
            color: #1B4079;
            padding: 0.25em 0.6em;
            border-radius: 8px;
            font-weight: bold;
        }

        .badge-processed {
            background-color: #079C34;
            color: #FFFFFF;
            padding: 0.25em 0.6em;
            border-radius: 8px;
            font-weight: bold;
        }

        .pagination-wrapper {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 2rem;
            width: 100%;
        }
        .pagination-left { text-align: left; flex: 1; }
        .pagination-center { text-align: center; flex: 1; font-weight: 600; color: #1B4079; }
        .pagination-right { text-align: right; flex: 1; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# 🚄 EN-TÊTE (Windows + Streamlit Cloud)
# ---------------------------------------------------
def get_base64_image(image_path: Path):
    with open(image_path, "rb") as f:
        return b64encode(f.read()).decode()

local_logo = Path(r"C:\\Users\\harri\\Desktop\\IT_MelvineYnov\\assets\\sncf_logo.png")
cloud_logo = Path("assets/sncf_logo.png")
logo_path = local_logo if local_logo.exists() else cloud_logo

header_html = "<div class='header-box'>"
if logo_path.exists():
    logo_b64 = get_base64_image(logo_path)
    header_html += f"<div class='main-logo'><img src='data:image/png;base64,{logo_b64}'></div>"
else:
    header_html += "<div class='main-logo'><h3>🚄 SNCF RH</h3></div>"

header_html += """
    <div class='main-title'>SNCF Confidential</div>
    <div class='subtitle'>Interface d’analyse et d’anonymisation automatique des candidatures.</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)
st.markdown("---")

# ---------------------------------------------------
# 📂 LECTURE DU FICHIER EXCEL (Windows + Cloud)
# ---------------------------------------------------
@st.cache_data
def load_excel(path: Path):
    return pd.read_excel(path)

# ✅ Correction : bon sous-dossier pour le fichier
local_excel = Path(r"C:\\Users\\harri\\Desktop\\IT_MelvineYnov\\data\\metadata\\cv_metadata_llama3.xlsx")
cloud_excel = Path("data/metadata/cv_metadata_llama3.xlsx")

excel_path = local_excel if local_excel.exists() else cloud_excel

if not excel_path.exists():
    st.error(f"⚠️ Le fichier Excel est introuvable. Vérifie le chemin : {excel_path}")
    st.stop()

df = load_excel(excel_path)
if "Profil" not in df.columns:
    df["Profil"] = "Not Processed"

# ---------------------------------------------------
# 🔄 GESTION DU STATE DES PROFILS
# ---------------------------------------------------
if "profil_status" not in st.session_state:
    st.session_state.profil_status = df["Profil"].to_dict()

cols_to_hide = ["Nom", "Email"]
df_display = df.drop(columns=[c for c in cols_to_hide if c in df.columns])

# ---------------------------------------------------
# ⚙️ PARAMÈTRES D’AFFICHAGE
# ---------------------------------------------------
with st.sidebar.expander("⚙️ Paramètres d’affichage", expanded=False):
    profiles_per_page = st.number_input("Nombre de candidatures par page :", min_value=5, max_value=15, value=8, step=1)

total_profiles = len(df_display)
total_pages = (total_profiles - 1) // profiles_per_page + 1
if "current_page" not in st.session_state:
    st.session_state.current_page = 1

current_page = st.session_state.current_page
start_idx = (current_page - 1) * profiles_per_page
end_idx = start_idx + profiles_per_page
current_profiles = df_display.iloc[start_idx:end_idx]

# ---------------------------------------------------
# 🧹 FONCTIONS DE NETTOYAGE
# ---------------------------------------------------
def clean_text(text):
    if pd.isna(text):
        return ""
    parts = re.split(r'[|,;]', str(text))
    cleaned = list(dict.fromkeys([p.strip().capitalize() for p in parts if p.strip()]))
    return " | ".join(cleaned)

def display_field(label, value):
    if value and str(value).strip():
        st.markdown(f"<div class='cv-section'><b>{label} :</b> {value}</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# 📋 AFFICHAGE DES PROFILS
# ---------------------------------------------------
for idx, candidate in current_profiles.iterrows():
    candidate_id = candidate.get("ID", f"ID_{idx}")
    profil_status = st.session_state.profil_status.get(idx, "Not Processed")
    cv_link = str(candidate.get("Lien", "")).strip()

    badge_html = '<span class="badge-processed">Processed</span>' if profil_status == "Processed" else '<span class="badge-not">Not Processed</span>'

    with st.container():
        st.markdown(f"""
        <div class="cv-card">
            <h3>CV Candidat {candidate_id} {badge_html}</h3>
            <p><b>Lien :</b> {cv_link}</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Curriculum Vitae Anonymisé"):
            poste = clean_text(candidate.get("Poste", ""))
            tel = clean_text(candidate.get("Téléphone", ""))
            langues = clean_text(candidate.get("Langues", ""))
            competences = clean_text(candidate.get("Compétences", ""))
            formation = clean_text(candidate.get("Formation", ""))
            experiences = clean_text(candidate.get("Expériences", ""))

            st.markdown("<div class='word-sheet'><h2 style='color:#000000;margin-bottom:1rem;'>Curriculum Vitae Anonymisé</h2>", unsafe_allow_html=True)
            display_field("Nom", "[FLOUTÉ]")
            display_field("Email", "[FLOUTÉ]")
            display_field("Téléphone", tel)
            display_field("Poste visé", poste)
            display_field("Langues parlées", langues)
            display_field("Compétences clés", competences)
            display_field("Formation", formation)
            display_field("Expériences principales", experiences)
            st.markdown("</div>", unsafe_allow_html=True)

            if st.button(f"✅ Terminer le traitement du candidat {candidate_id}", key=f"btn_{idx}"):
                st.session_state.profil_status[idx] = "Processed"
                st.success(f"Candidat {candidate_id} marqué comme traité ✅.")
                st.rerun()

st.markdown("---")

# ---------------------------------------------------
# ⏩ PAGINATION ALIGNÉE
# ---------------------------------------------------
st.markdown("<div class='pagination-wrapper'>", unsafe_allow_html=True)
col_left, col_center, col_right = st.columns([1, 3, 1])

with col_left:
    if st.button("⬅️ Précédent") and current_page > 1:
        st.session_state.current_page -= 1
        st.rerun()

with col_center:
    st.markdown(f"<div class='pagination-center'>Page {current_page} / {total_pages}</div>", unsafe_allow_html=True)

with col_right:
    if st.button("➡️ Suivant") and current_page < total_pages:
        st.session_state.current_page += 1
        st.rerun()

st.markdown("</div>", unsafe_allow_html=True)
