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
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FF007F !important;
        font-family: sans-serif !important;
    }

    [data-testid="stSidebar"] { 
        background-color: #FFC0CB !important; 
    }

    [data-testid="stSidebar"] summary svg { display: none !important; }
    
    [data-testid="stSidebar"] summary {
        color: #800040 !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
        list-style: none !important;
    }

    [data-testid="stSidebar"] label, [data-testid="stSidebar"] p {
        color: #800040 !important;
    }

    .stButton > button {
        background-color: #FFF333 !important;
        border: 3px solid #000000 !important;
        border-radius: 20px !important;
    }
    
    .stButton > button div p {
        color: #000000 !important;
        font-weight: 900 !important;
        font-size: 18px !important;
    }

    h1, h2, h3, [data-testid="stSubheader"] p { 
        color: #FFF333 !important; 
    }

    [data-testid="stMetric"] {
        background-color: #FFF333 !important;
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

# --- MENU LATÉRAL (CONFIG) ---
with st.sidebar:
    st.markdown("### ⚙️ CONFIG")
    
    with st.expander("💖 AJOUTER ENVELOPPE", expanded=False):
        nom = st.text_input("Nom")
        budget = st.number_input("Budget (€)", min_value=0.0)
        if st.button("CRÉER"):
            if nom:
                st.session_state.enveloppes[nom] = {'budget': budget, 'spent': 0.0}
                save_data()
                st.rerun()

    with st.expander("⭐ OBJECTIF ÉPARGNE", expanded=False):
        st.session_state.epargne["nom"] = st.text_input("Nom", value=st.session_state.epargne["nom"])
        st.session_state.epargne["objectif"] = st.number_input("Cible (€)", value=float(st.session_state.epargne["objectif"]))
        st.session_state.epargne["actuel"] = st.number_input("Actuel (€)", value=float(st.session_state.epargne["actuel"]))
        if st.button("SAUVER CONFIG"):
            save_data()
            st.toast("Épargne à jour !")

    st.markdown("---")
    
    # NOUVELLE SECTION : SUPPRESSION
    if st.session_state.enveloppes:
        with st.expander("🗑️ SUPPRIMER UNE ENVELOPPE"):
            to_delete = st.selectbox("Laquelle ?", list(st.session_state.enveloppes.keys()))
            if st.button("EFFACER DÉFINITIVEMENT"):
                del st.session_state.enveloppes[to_delete]
                save_data()
                st.rerun()

    # NOUVELLE SECTION : NOUVEAU MOIS
    st.markdown("---")
    if st.button("🗓️ NOUVEAU MOIS"):
        for env in st.session_state.enveloppes:
            st.session_state.enveloppes[env]['spent'] = 0.0
        save_data()
        st.balloons()
        st.success("C'est reparti pour un mois ! 🚀")
        st.rerun()

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.info("Ouvre le menu à gauche pour créer tes enveloppes ! ✨")
else:
    st.subheader("Dépenses du jour ?")
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.5)
    with col2:
        cat = st.selectbox("Enveloppe", list(st.session_state.enveloppes.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔥 VALIDER"):
            st.session_state.enveloppes[cat]['spent'] += montant
            save_data()
            st.toast(f"-{montant}€ sur {cat}")
            st.rerun()
    with c2:
        if st.button("☀️ RIEN"):
            st.balloons()
            st.success("BIEN JOUÉ ! 🏆")

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
