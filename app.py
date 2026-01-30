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
    /* Import d'une police ronde et fun qui marche partout */
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@700&display=swap');

    .stApp { background-color: #FF007F; } 
    
    [data-testid="stSidebar"] { background-color: #FFC0CB !important; }
    
    /* Police globale forcée */
    h1, h2, h3, p, span, label, div { 
        font-family: 'Fredoka', 'Comic Sans MS', sans-serif !important; 
        font-weight: bold;
    }

    /* Couleurs textes Dashboard */
    h1, h2, h3, p, span, label { color: #FFF333 !important; }

    /* Textes Sidebar en Rose Foncé */
    [data-testid="stSidebar"] .stMarkdown p, 
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] label {
        color: #FF007F !important;
    }

    /* BOUTONS : Texte Noir pour la lisibilité sur Jaune */
    .stButton>button { 
        background-color: #FFF333 !important; 
        color: #000000 !important; /* NOIR pour bien voir */
        border-radius: 50px; 
        border: 4px solid #000000;
        font-size: 18px !important;
        font-weight: 900 !important;
        transition: 0.3s;
    }
    
    /* Inputs et Selectbox */
    input { background-color: #FFF333 !important; color: #000000 !important; }
    div[data-baseweb="select"] > div { background-color: #FFF333 !important; color: #000000 !important; }

    .stMetric { 
        background-color: rgba(255, 243, 51, 0.2); 
        padding: 15px; border-radius: 15px; border: 2px solid #FFF333; 
    }
    
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
    st.title("⚙️ Ma Config")
    with st.expander("Ajouter une enveloppe"):
        nom = st.text_input("Nom (ex: Courses)")
        budget = st.number_input("Montant mensuel (€)", min_value=0.0)
        if st.button("Créer"):
            st.session_state.enveloppes[nom] = {'budget': budget, 'spent': 0.0}
            save_data()
            st.rerun()
            
    with st.expander("Objectif Épargne"):
        st.session_state.epargne["nom"] = st.text_input("Nom de l'objectif", value=st.session_state.epargne["nom"])
        st.session_state.epargne["objectif"] = st.number_input("Montant cible (€)", value=st.session_state.epargne["objectif"])
        st.session_state.epargne["actuel"] = st.number_input("Déjà épargné (€)", value=st.session_state.epargne["actuel"])
        if st.button("Sauver"):
            save_data()
            st.toast("Épargne sauvée !")

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.warning("Crée tes enveloppes à gauche ! 👈")
else:
    st.subheader("Dépenses du jour ?")
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.5, key="new_spent")
    with col2:
        cat = st.selectbox("Enveloppe", list(st.session_state.enveloppes.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔥 VALIDER"):
            st.session_state.enveloppes[cat]['spent'] += montant
            save_data()
            st.toast(f"Boom ! -{montant}€")
            st.rerun()
    with c2:
        if st.button("☀️ RIEN"):
            st.balloons()
            st.success("BIEN JOUÉ ! 🏆")

    st.divider()
    st.header("📍 Où j'en suis")
    
    for name, data in st.session_state.enveloppes.items():
        reste = data['budget'] - data['spent']
        progress = min(data['spent'] / data['budget'], 1.0) if data['budget'] > 0 else 0
        st.metric(label=f"Enveloppe {name}", value=f"{reste}€", delta=f"sur {data['budget']}€", delta_color="off")
        st.progress(progress)
    
    st.divider()
    ep = st.session_state.epargne
    prog_ep = min(ep['actuel'] / ep['objectif'], 1.0) if ep['objectif'] > 0 else 0
    st.subheader(f"⭐ {ep['nom']}")
    st.metric("Total épargné", f"{ep['actuel']}€", f"Objectif: {ep['objectif']}€")
    st.progress(prog_ep)
