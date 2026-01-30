import streamlit as st
import pandas as pd

# --- CONFIGURATION LOOK ---
st.set_page_config(page_title="Point Thunes !", page_icon="💖")

# CSS pour le look Rose & Jaune
st.markdown("""
    <style>
    .stApp { background-color: #FF007F; } /* Fond Rose Vibrant */
    [data-testid="stHeader"] { background-color: rgba(0,0,0,0); }
    h1, h2, h3, p, span, label { color: #FFF333 !important; font-family: 'Comic Sans MS', cursive, sans-serif; font-weight: bold; }
    .stButton>button { 
        background-color: #FFF333; color: #FF007F; 
        border-radius: 50px; border: 3px solid black;
        font-size: 20px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.05); background-color: #ffffff; }
    input { background-color: #FFF333 !important; color: #FF007F !important; }
    .stMetric { background-color: rgba(255, 243, 51, 0.2); padding: 15px; border-radius: 15px; border: 2px solid #FFF333; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION ---
if 'enveloppes' not in st.session_state:
    st.session_state.enveloppes = {}
if 'epargne' not in st.session_state:
    st.session_state.epargne = {"nom": "Épargne", "objectif": 0.0, "actuel": 0.0}

# --- MENU LATÉRAL (CONFIGURATION) ---
with st.sidebar:
    st.title("⚙️ Ma Config")
    with st.expander("Ajouter une enveloppe"):
        nom = st.text_input("Nom (ex: Courses)")
        budget = st.number_input("Montant mensuel (€)", min_value=0.0)
        if st.button("Créer l'enveloppe"):
            st.session_state.enveloppes[nom] = {'budget': budget, 'spent': 0.0}
            st.rerun()
            
    with st.expander("Objectif Épargne"):
        st.session_state.epargne["nom"] = st.text_input("Nom de l'objectif", value=st.session_state.epargne["nom"])
        st.session_state.epargne["objectif"] = st.number_input("Montant cible (€)", value=st.session_state.epargne["objectif"])
        st.session_state.epargne["actuel"] = st.number_input("Déjà épargné (€)", value=st.session_state.epargne["actuel"])

# --- ÉCRAN PRINCIPAL ---
st.title("💖 POINT THUNES !")

if not st.session_state.enveloppes:
    st.warning("Commence par créer tes enveloppes dans le menu à gauche ! 👈")
else:
    # --- SAISIE DU JOUR ---
    st.subheader("Combien as-tu dépensé aujourd'hui ?")
    col1, col2 = st.columns(2)
    with col1:
        montant = st.number_input("Montant (€)", min_value=0.0, step=0.5, key="new_spent")
    with col2:
        cat = st.selectbox("Enveloppe", list(st.session_state.enveloppes.keys()))
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔥 Valider la dépense"):
            st.session_state.enveloppes[cat]['spent'] += montant
            st.toast(f"Boom ! -{montant}€ pour {cat}")
    with c2:
        if st.button("☀️ Rien dépensé !"):
            st.balloons()
            st.success("BIEN JOUÉ ! Championne ! 🏆")

    # --- DASHBOARD ---
    st.divider()
    st.header("📍 Où j'en suis")
    
    for name, data in st.session_state.enveloppes.items():
        reste = data['budget'] - data['spent']
        progress = min(data['spent'] / data['budget'], 1.0) if data['budget'] > 0 else 0
        
        st.metric(label=f"Enveloppe {name}", value=f"{reste}€", delta=f"sur {data['budget']}€", delta_color="off")
        st.progress(progress)
    
    # --- ÉPARGNE ---
    st.divider()
    ep = st.session_state.epargne
    prog_ep = min(ep['actuel'] / ep['objectif'], 1.0) if ep['objectif'] > 0 else 0
    st.subheader(f"⭐ {ep['nom']}")
    st.metric("Total épargné", f"{ep['actuel']}€", f"Objectif: {ep['objectif']}€")
    st.progress(prog_ep)
