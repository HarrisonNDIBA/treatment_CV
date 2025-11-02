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
# 🎨 STYLE SNCF AVEC PHOTO DANS LA ZONE BLANCHE DU BAS
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
            margin-bottom: 1.5rem;
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

        /* ✅ Style pour le texte de l'offre (sans boîte) */
        .offre-text {
            font-size: 1.05rem;
            color: #1B4079;
            text-align: center;
            margin: 1rem auto 2rem auto;
            line-height: 1.6;
            max-width: 900px;
        }

        .offre-text b {
            color: #000000;
        }

        .cv-card {
            background-color: #7F9C96;
            border-radius: 12px;
            padding: 1.6rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 3px 8px rgba(27,64,121,0.15);
            border-left: 6px solid #1B4079;
            position: relative;
        }

        .cv-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .cv-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .cv-left img {
            width: 55px;
            height: 55px;
            border-radius: 50%;
            border: 2px solid #1B4079;
            background-color: white;
            object-fit: cover;
        }

        .cv-card h3 {
            color: #FFFFFF;
            margin-bottom: 0.6rem;
            display: inline-block;
        }

        .cv-card p { color: #F7F7F7; }

        .word-sheet {
            background-color: #FFFFFF;
            border-radius: 10px;
            padding: 1.5rem;
            padding-right: 200px;
            box-shadow: 0 2px 8px rgba(27,64,121,0.1);
            line-height: 1.7;
            color: #000000;
            margin-top: 0.8rem;
            border-left: 5px solid #8FAD88;
            position: relative;
        }

        .photo-frame {
            position: absolute;
            bottom: -170px;
            right: -20px;
            width: 100px;
            height: 130px;
            background-color: #000;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            border: 3px solid #1B4079;
            display: flex;
            justify-content: center;
            align-items: center;
            color: white;
            font-weight: bold;
        }

        .photo-frame::after {
            content: "PHOTO";
            font-size: 1rem;
            letter-spacing: 1px;
        }

        .cv-section {
            border-bottom: 1px solid #D9D9D9;
            padding: 0.6rem 0;
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
            padding: 0.3em 0.8em;
            border-radius: 8px;
            font-weight: bold;
            font-size: 0.9rem;
        }

        .badge-processed {
            background-color: #079C34;
            color: #FFFFFF;
            padding: 0.3em 0.8em;
            border-radius: 10px;
            font-weight: bold;
            font-size: 0.9rem;
        }

        hr.separator {
            border: none;
            border-top: 3px solid #1B4079;
            margin: 2rem 0;
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
# 🚄 EN-TÊTE
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
    <div class='main-title'>Automatisation_RH</div>
    <div class='subtitle'>Interface d’analyse et d’anonymisation automatique des candidatures.</div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ✅ Texte OFFRE ajouté juste après la boîte du titre, sans encadrement
st.markdown("""
<div class='offre-text'>
    <b>OFFRE :</b> Nous recherchons un Data Analyst maîtrisant <b>Python</b>, <b>SQL</b>, <b>Power BI</b> et <b>Excel</b>.<br>
    Capable de réaliser des analyses de données, dashboards et rapports, avec une expérience en machine learning et cloud.
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------------------------------------------------
# 📂 LECTURE DU FICHIER EXCEL
# ---------------------------------------------------
@st.cache_data
def load_excel(path: Path):
    return pd.read_excel(path)

local_excel = Path(r"C:\\Users\\harri\\Desktop\\IT_MelvineYnov\\data\\metadata\\cv_metadata_llama3.xlsx")
cloud_excel = Path("data/metadata/cv_metadata_llama3.xlsx")

if local_excel.exists():
    excel_path = local_excel
elif cloud_excel.exists():
    excel_path = cloud_excel
else:
    st.error("⚠️ Aucun fichier Excel trouvé.")
    st.stop()

df = load_excel(excel_path)
if "Profil" not in df.columns:
    df["Profil"] = "Not Processed"

if "profil_status" not in st.session_state:
    st.session_state.profil_status = df["Profil"].to_dict()

cols_to_hide = ["Nom", "Email"]
df_display = df.drop(columns=[c for c in cols_to_hide if c in df.columns])


# ---------------------------------------------------
# 🧹 OUTILS
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
# 🧍‍♂️ AVATAR NEUTRE
# ---------------------------------------------------
avatar_path = Path(r"C:\\Users\\harri\\Desktop\\IT_MelvineYnov\\assets\\neutral_avatar.png")
if avatar_path.exists():
    avatar_b64 = get_base64_image(avatar_path)
    avatar_html = f"<img src='data:image/png;base64,{avatar_b64}'>"
else:
    avatar_html = "<div style='width:55px;height:55px;border-radius:50%;background:#FFF;border:2px solid #1B4079;'></div>"

# ---------------------------------------------------
# 📋 AFFICHAGE DES CANDIDATS AVEC PAGINATION
# ---------------------------------------------------
profiles_per_page = 8
total_profiles = len(df_display)
total_pages = (total_profiles - 1) // profiles_per_page + 1

if "current_page" not in st.session_state:
    st.session_state.current_page = 1

current_page = st.session_state.current_page
start_idx = (current_page - 1) * profiles_per_page
end_idx = start_idx + profiles_per_page
current_profiles = df_display.iloc[start_idx:end_idx]

for idx, candidate in current_profiles.iterrows():
    candidate_number = idx + 1
    profil_status = st.session_state.profil_status.get(idx, "Not Processed")
    cv_link = str(candidate.get("Lien", "")).strip()

    badge_html = (
        '<span class="badge-processed">Processed</span>'
        if profil_status == "Processed"
        else '<span class="badge-not">Not Processed</span>'
    )

    poste = clean_text(candidate.get("Poste", ""))
    tel = clean_text(candidate.get("Téléphone", ""))
    langues = clean_text(candidate.get("Langues", ""))
    competences = clean_text(candidate.get("Compétences", ""))
    formation = clean_text(candidate.get("Formation", ""))
    experiences = clean_text(candidate.get("Expériences", ""))

    with st.container():
        st.markdown(f"""
        <div class="cv-card">
            <div class="cv-header">
                <div class="cv-left">
                    {avatar_html}
                    <h3>Candidat n°{candidate_number}</h3>
                </div>
                <div class="cv-right">
                    {badge_html}
                </div>
            </div>
            <p><b>Lien :</b> {cv_link}</p>
            <div class='word-sheet'>
                <h2 style='color:#000000;margin-bottom:1rem;'>Curriculum Vitae Anonymisé</h2>
                <div class='photo-frame'></div>
        """, unsafe_allow_html=True)

        display_field("Nom", "[FLOUTÉ]")
        display_field("Email", "[FLOUTÉ]")
        display_field("Téléphone", tel)
        display_field("Poste visé", poste)
        display_field("Langues parlées", langues)
        display_field("Compétences clés", competences)
        display_field("Formation", formation)
        display_field("Expériences principales", experiences)

        st.markdown("</div>", unsafe_allow_html=True)

        if st.button(f"✅ Terminer le traitement du candidat {candidate_number}", key=f"btn_{idx}"):
            st.session_state.profil_status[idx] = "Processed"
            st.success(f"Candidat n°{candidate_number} marqué comme traité ✅.")
            st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='separator'>", unsafe_allow_html=True)

# ---------------------------------------------------
# ⏩ PAGINATION
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
