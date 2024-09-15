import streamlit as st

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

st.write("# Bienvenue sur Tweets Analysis!👋")
st.markdown(
    """
    ## Interface web : Analyse avancée des Tweets
    L’objectif de ce projet est d'aborder ce problème afin de répondre 
    de manière efficace aux différents challenges posés par ce type de données textuelles aux méthodes 
    basées sur des modèles probabilistes ou sur la factorisation matricielle.

    ### Réalisations attendues: 
    1. Constitution d’un benchmark de données Tweets à partir de Twitter
    2. Création d’une Interface web avec Python Dash, Streamlit, ou R shiny pour l’analyse des Tweets
    3. Implémentation des méthodes de nettoyage de tweets et intégration à l’interface web
    4. Utilisation des approches de “Topics modeling” (LDA, NMF) et intégration à l’interface web
    """
)

st.write("")
st.write("")
st.write("Réalisé par : Rose-Milca CENAT")