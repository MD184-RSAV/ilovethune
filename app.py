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
    /* 1. POLICE ET FOND */
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif !important;
        background-color: #FF007F !important;
    }

    /* 2. SIDEBAR : NETTOYAGE RADICAL */
    [data-testid="stSidebar"] { 
        background-color: #FFC0CB !important; 
    }
    
    /* Supprime le texte fantôme jaune/superposé dans les expanders */
    [data-testid="stSidebar"] summary div p {
        display: none !important;
    }
    
    /* Force un seul titre propre pour les expanders */
    [data-testid="stSidebar"] summary span {
        color: #800040 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }

    /* Couleurs des labels et textes dans la sidebar */
    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #800040 !important;
        text-shadow: none !important;
    }

    /* 3. BOUTONS : Look Flashy et Lisible */
    .stButton > button {
        background-color: #FFF333 !important;
        color: #000000 !important;
        border: 3px solid #000000 !important;
        border-radius: 20px !important;
        font-weight: 900 !important;
        text-transform: uppercase;
    }
    
    .stButton > button div p {
        color: #000000 !important;
        font-size: 18px !important;
    }

    /* 4. ÉCRAN PRINCIPAL */
    h1, h2, h3, [data-testid="stMarkdownContainer"] p { 
        color: #FFF333 !important; 
    }
    
    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #FFF333 !important;
        border: 3px solid #000000 !important;
        border-radius: 15px !important;
        color: #000000 !important;
    }
    [data-testid="stMetricLabel"] p { color: #000000 !important; }
    [data-testid="stMetricValue"] div { color: #FF007F !important; }

    /* Barres de progression */
    .stProgress > div > div > div > div { background-color: #FFF333 !important; }
    
    /* Inputs */
    input { background-color: #ffffff !important; color: #000000 !important; border: 2px solid #800040 !important; }
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
    st.markdown("# ⚙️ CONFIG")
    
    # Expander 1
    with st.expander("Ajouter une enveloppe", expanded=False):
        nom = st.text_input("Nom de l'enveloppe", key="add_nom")
        budget = st.number_input("Budget mensuel (€)", min_value=0.0, key="add_budget")
        if st.button("CRÉER"):
            if nom:
                st.session_state.enveloppes[nom] = {'budget': budget, 'spent': 0.0}
                save_data()
                st.rerun()
            
    # Expander 2
    with st.expander("Objectif Épargne", expanded=False):
        st.session_state.epargne["nom"] = st.text_input("Nom de l'objectif", value=st.session_state.epargne["nom"])
        st.session_state.epargne["objectif"] = st.number_input("Montant cible", value=float(st.session_state.epargne["objectif"]))
        st.session_state.epargne["actuel"] = st.number_input("Déjà épargné", value=float(st.session_state.epargne["actuel"]))
        if st.button("SAUVER"):
            save_data()
            st.toast("Épargne mise à jour !")

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.info("Ouvre le menu à gauche pour commencer !")
else:
    st.subheader("Dépenses du jour ?")
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.5, key="main_input")
    with col2:
        cat = st.selectbox("Dans quelle enveloppe ?", list(st.session_state.enveloppes.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔥 VALIDER"):
            st.session_state.enveloppes[cat]['spent'] += montant
            save_data()
            st.toast(f"Enregistré : -{montant}€")
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
