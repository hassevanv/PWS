import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from ultimate_ttt import simulate_games  # Hier importeren we jouw logica!

st.set_page_config(page_title="PWS Ultimate Tic Tac Toe", layout="wide")

st.title("Ultimate Tic Tac Toe Simulatie")
st.markdown("Dashboard voor PWS Simulaties")

# Gebruikersinvoer in de zijbalk
with st.sidebar:
    st.header("Instellingen")
    n_games = st.slider("Aantal potjes om te simuleren", 100, 1000000, 1000)
    run_btn = st.button("Start Simulatie")

if run_btn:
    with st.spinner('Simulatie draait...'):
        # Roep de functie aan uit ultimate_ttt.py
        stats = simulate_games(n_games)
        
    # Resultaten tonen
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Resultaten")
        df = pd.DataFrame({
            "Speler": ["X", "O", "Gelijkspel"],
            "Winsten": [stats['X'], stats['O'], stats['Draw']]
        })
        st.table(df)

    with col2:
        st.subheader("Verdeling")
        fig, ax = plt.subplots()
        ax.pie(df["Winsten"], labels=df["Speler"], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99'])
        st.pyplot(fig)
        
    st.success(f"Klaar! {n_games} potjes gesimuleerd.")