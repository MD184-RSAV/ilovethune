import streamlit as st
import json
import os

# --- PERSISTENCE DES DONNÉES ---
DB_FILE = "data_budget.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {"enveloppes": {}, "epargne": {"nom": "Épargne", "objectif": 0.0, "actuel": 0.0}}

def save_data():
    data = {
        "enveloppes": st.session_state.enveloppes,
        "epargne": st.session_state.epargne
    }
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

# --- INITIALISATION ---
if 'data_loaded' not in st.session_state:
    loaded = load_data()
    st.session_state.enveloppes = loaded["enveloppes"]
    st.session_state.epargne = loaded["epargne"]
    st.session_state.data_loaded = True

# --- CONFIGURATION LOOK ---
st.set_page_config(page_title="Point Thunes !", page_icon="💖")

st.markdown("""
    <style>
    .stApp { background-color: #FF007F; } 
    h1, h2, h3, p, span, label { color: #FFF333 !important; font-family: 'Arial Black', sans-serif; }
    .stButton>button { 
        background-color: #FFF333; color: #FF007F; 
        border-radius: 50px; border: 4px solid black;
        font-size: 22px; font-weight: bold; width: 100%;
    }
    .stMetric { background-color: #FFF333; padding: 10px; border-radius: 10px; border: 3px solid black; }
    /* Style des barres de progression */
    .stProgress > div > div > div > div { background-color: #FFF333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- MENU LATÉRAL (CONFIG) ---
with st.sidebar:
    st.title("⚙️ CONFIG")
    nom_env = st.text_input("Nom de l'enveloppe")
    budget_env = st.number_input("Budget (€)", min_value=0.0)
    if st.button("➕ AJOUTER"):
        st.session_state.enveloppes[nom_env] = {'budget': budget_env, 'spent': 0.0}
        save_data()
        st.rerun()
    
    st.divider()
    if st.button("🗑️ RESET TOUT (Attention)"):
        st.session_state.enveloppes = {}
        save_data()
        st.rerun()

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.info("Utilise le menu à gauche pour créer ta première enveloppe ! ✨")
else:
    # --- SAISIE RAPIDE ---
    with st.container():
        st.subheader("Combien as-tu dépensé aujourd'hui ?")
        m_col, e_col = st.columns(2)
        with m_col:
            montant = st.number_input("Somme (€)", min_value=0.0, step=1.0)
        with e_col:
            cat = st.selectbox("Enveloppe", list(st.session_state.enveloppes.keys()))
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("🔥 VALIDÉ"):
                st.session_state.enveloppes[cat]['spent'] += montant
                save_data()
                st.toast(f"Enregistré ! -{montant}€")
                st.rerun()
        with btn_col2:
            if st.button("☀️ RIEN !"):
                st.balloons()
                st.success("BIEN JOUÉ ! 🏆")

    # --- DASHBOARD ---
    st.markdown("---")
    st.header("📍 MES COMPTES")
    
    for name, data in st.session_state.enveloppes.items():
        reste = data['budget'] - data['spent']
        ratio = min(data['spent'] / data['budget'], 1.0) if data['budget'] > 0 else 0
        
        col_txt, col_met = st.columns([2, 1])
        with col_txt:
            st.write(f"**{name}**")
            st.progress(ratio)
        with col_met:
            st.metric("Reste", f"{reste}€")

# --- SECTION ÉPARGNE ---
st.markdown("---")
st.subheader("⭐ ÉPARGNE")
# Ici on pourrait ajouter une logique similaire pour l'épargne
