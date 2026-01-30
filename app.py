import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Point Thunes !", page_icon="💰")

# --- STYLE PERSONNALISÉ (JAUNE & ROSE) ---
st.markdown("""
    <style>
    .main { background-color: #FFF333; } /* Fond Jaune */
    h1, h2, h3 { color: #FF007F !important; font-family: 'Arial Black'; } /* Texte Rose */
    .stButton>button { 
        background-color: #FF007F; 
        color: white; 
        border-radius: 20px; 
        border: 2px solid black;
        font-weight: bold;
    }
    .stMetric { background-color: white; padding: 15px; border-radius: 15px; border: 3px solid #FF007F; }
    </style>
    """, unsafe_allow_html=True)

# --- INITIALISATION DES DONNÉES ---
if 'enveloppes' not in st.session_state:
    st.session_state.enveloppes = {
        'Courses': {'budget': 400.0, 'spent': 0.0},
        'Loisirs': {'budget': 150.0, 'spent': 0.0},
        'Epargne': {'budget': 2000.0, 'spent': 1200.0} # Objectif atteint progressivement
    }

# --- TITRE ---
st.title("💖 Point Thunes !")

# --- ÉCRAN DE SAISIE QUOTIDIENNE ---
st.header("Combien as-tu dépensé aujourd'hui ?")

with st.expander("Saisir une dépense", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        amount = st.number_input("Montant (€)", min_value=0.0, step=1.0)
    with col2:
        cat = st.selectbox("Dans quelle enveloppe ?", list(st.session_state.enveloppes.keys()))
    
    place = st.text_input("Où ? (ex: Monoprix, Cinéma)")
    
    if st.button("Valider la dépense"):
        st.session_state.enveloppes[cat]['spent'] += amount
        st.success(f"Enregistré : {amount}€ déduits de {cat} ! ✨")

if st.button("☀️ Je n'ai rien dépensé aujourd'hui"):
    st.balloons()
    st.markdown("### **Bien joué !** Tes économies te disent merci. 🏆")

# --- DASHBOARD DES ENVELOPPES ---
st.divider()
st.header("Mes Enveloppes")

for name, data in st.session_state.enveloppes.items():
    reste = data['budget'] - data['spent']
    progress = min(data['spent'] / data['budget'], 1.0)
    
    col_a, col_b = st.columns([1, 3])
    with col_a:
        st.metric(label=name, value=f"{reste}€", delta=f"Total: {data['budget']}€")
    with col_b:
        st.write(f"Progression : {int(progress*100)}%")
        st.progress(progress)

# --- SECTION ÉPARGNE SPÉCIALE ---
st.divider()
st.subheader("⭐ Objectif Épargne")
e_data = st.session_state.enveloppes['Epargne']
st.write(f"Cagnotte actuelle : **{e_data['spent']}€** sur un objectif de **{e_data['budget']}€**")
st.progress(min(e_data['spent'] / e_data['budget'], 1.0))
