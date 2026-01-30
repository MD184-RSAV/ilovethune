import streamlit as st
import json
import os

# --- LOGIQUE DE SAUVEGARDE ---
DB_FILE = "mes_thunes_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return None

def save_data():
    data = {
        "enveloppes": st.session_state.enveloppes,
        "epargne": st.session_state.epargne
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- CONFIGURATION LOOK ---
st.set_page_config(page_title="Point Thunes !", page_icon="💖")

st.markdown("""
    <style>
    /* 1. RESET COMPLET & POLICE UNIQUE */
    html, body, [data-testid="stAppViewContainer"], .stMarkdown, label, span {
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif !important;
    }

    /* 2. FOND PRINCIPAL */
    .stApp { background-color: #FF007F !important; } 
    
    /* 3. SIDEBAR : On nettoie le bazar visuel */
    [data-testid="stSidebar"] { 
        background-color: #FFC0CB !important; 
    }
    
    /* On force les textes du sidebar en noir/rose foncé pour stopper la superposition jaune */
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] label, 
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #800040 !important; 
        font-size: 1rem !important;
        text-shadow: none !important;
    }

    /* 4. BOUTONS : On les rend ENFIN lisibles */
    .stButton > button {
        background-color: #FFF333 !important;
        color: #000000 !important; /* Texte Noir */
        border: 3px solid #000000 !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        height: 3em !important;
        width: 100% !important;
        display: block !important;
    }
    
    /* Correction spécifique pour le texte dans le bouton qui disparaît */
    .stButton > button p {
        color: #000000 !important;
        margin: 0 !important;
        font-size: 18px !important;
    }

    /* 5. TITRES ÉCRAN PRINCIPAL */
    h1, h2, h3, .stSubheader p { 
        color: #FFF333 !important; 
        text-shadow: 2px 2px 0px #000000;
    }

    /* 6. CHAMPS DE SAISIE */
    input, div[data-baseweb="select"] {
        background-color: #FFF333 !important;
    }
    div[data-baseweb="select"] span {
        color: #000000 !important; /* Texte noir dans les listes */
    }

    /* 7. METRICS & PROGRESS */
    .stMetric { 
        background-color: rgba(255, 243, 51, 0.9) !important; 
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
    }
    [data-testid="stMetricLabel"] p { color: #000000 !important; }
    [data-testid="stMetricValue"] div { color: #FF007F !important; }
    
    .stProgress > div > div > div > div { background-color: #FFF333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'enveloppes' not in st.session_state:
    saved_data = load_data()
    if saved_data:
        st.session_state.enveloppes = saved_data["enveloppes"]
        st.session_state.epargne = saved_data["epargne"]
    else:
        st.session_state.enveloppes = {}
        st.session_state.epargne = {"nom": "Épargne", "objectif": 0.0, "actuel": 0.0}

# --- MENU LATÉRAL ---
with st.sidebar:
    st.title("⚙️ CONFIG")
    with st.expander("Ajouter une enveloppe"):
        nom = st.text_input("Nom de l'enveloppe")
        budget = st.number_input("Budget mensuel (€)", min_value=0.0)
        if st.button("CRÉER"):
            st.session_state.enveloppes[nom] = {'budget': budget, 'spent': 0.0}
            save_data()
            st.rerun()
            
    with st.expander("Objectif Épargne"):
        st.session_state.epargne["nom"] = st.text_input("Nom de l'objectif", value=st.session_state.epargne["nom"])
        st.session_state.epargne["objectif"] = st.number_input("Montant cible", value=st.session_state.epargne["objectif"])
        st.session_state.epargne["actuel"] = st.number_input("Déjà épargné", value=st.session_state.epargne["actuel"])
        if st.button("SAUVER"):
            save_data()
            st.toast("Sauvegardé !")

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.warning("Ouvre le menu à gauche pour créer tes enveloppes !")
else:
    st.subheader("Dépenses du jour ?")
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.5, key="new_spent")
    with col2:
        cat = st.selectbox("Choisir l'enveloppe", list(st.session_state.enveloppes.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔥 VALIDER"):
            st.session_state.enveloppes[cat]['spent'] += montant
            save_data()
            st.toast(f"Payé ! -{montant}€")
            st.rerun()
    with c2:
        if st.button("☀️ RIEN"):
            st.balloons()
            st.success("BRAVO ! 💰")

    st.divider()
    st.header("📍 RÉCAP")
    
    for name, data in st.session_state.enveloppes.items():
        reste = data['budget'] - data['spent']
        progress = min(data['spent'] / data['budget'], 1.0) if data['budget'] > 0 else 0
        st.metric(label=f"Enveloppe {name}", value=f"{reste}€", delta=f"sur {data['budget']}€", delta_color="off")
        st.progress(progress)
    
    st.divider()
    ep = st.session_state.epargne
    prog_ep = min(ep['actuel'] / ep['objectif'], 1.0) if ep['objectif'] > 0 else 0
    st.subheader(f"⭐ {ep['nom']}")
    st.metric("Total épargné", f"{ep['actuel']}€", f"Cible: {ep['objectif']}€")
    st.progress(prog_ep)
