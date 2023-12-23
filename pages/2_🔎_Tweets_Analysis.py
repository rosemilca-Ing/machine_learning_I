import streamlit as st
import time
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt

from collections import Counter
from nltk.tokenize import word_tokenize

st.set_page_config(page_title="Tweets Analysis", page_icon="🔎")

if 'my_data_glob' not in st.session_state:
    st.session_state['my_data_glob'] = ''


st.markdown("# Tweets Analysis")
#st.sidebar.header("Plotting Demo")
st.write(
    """
    Dans cette partie nous ferons un peu d'analyse descriptive des tweets.
    """
)


# Fonction pour charger le fichier CSV
# @st.cache(allow_output_mutation=True)
@st.cache_data
def load_csv(file):
    df = pd.read_csv(file)
    return df


my_data = pd.DataFrame() # initialisation de la variable df

#Upload le fichier
uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

if uploaded_file is not None:
    # Stockage de la variable globale
    my_data = load_csv(uploaded_file) 
    st.session_state['my_data_glob'] = my_data   

    nb_tweets = len(my_data)
    st.markdown("#### Nombre de tweets : " + str(nb_tweets))
    st.markdown("#### Nombre de tweets par users (top 10)")
    top_n = 10 # par exemple
    top_users = my_data['username'].value_counts().head(top_n)
    st.write(top_users)

    st.write("")
    # Nous pouvons représenter graphiquement la liste des auteurs ayant posté 5 tweets ou plus.
    st.markdown("#### Users ayant posté 5 tweets ou plus(top 10)")
    # Filtrer les utilisateurs ayant posét 5 tweets ou plus
    selected_users = top_users[top_users >= 5]

    # Créer un diagramme à barres pour afficher le nombre de tweets pour chaque utilisateur sélectionné
    fig, ax = plt.subplots()
    ax.bar(selected_users.index, selected_users.values)
    ax.set_title("Nombre de tweets par utilisateur")
    ax.set_xlabel("Utilisateurs")
    ax.set_ylabel("Nombre de tweets")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)

    st.write("")
    # Hashtags les plus frequents
    st.markdown("#### Hashtags plus fréquents (top 10)")
 
    # Créer une fonction pour extraire les hashtags du texte des tweets
    def extract_hashtags(text):
        hashtags = re.findall(r'\#\w+', text)
        return hashtags

    # Créer une nouvelle colonne pour les hashtags
    my_data['hashtags'] = my_data['text'].apply(extract_hashtags)

    # Utiliser la fonction explode pour transformer la colonne de hashtags
    # en une série de hashtags individuels
    hashtags_series = my_data['hashtags'].explode()

    # Compter le nombre d'occurrences de chaque hashtag
    counts = hashtags_series.value_counts()

    # Afficher les 10 hashtags les plus fréquents
    top_hashtags = counts.head(10)
    st.write(top_hashtags)

    # mentions plus frequents

    # Extraire les mentions dans une nouvelle colonne 'mentions'
    my_data['mentions'] = my_data['text'].str.findall(r'(?<![@\w])@(\w{1,25})').apply(set)

    # Compter le nombre de fois que chaque mention apparaît
    mentions_count = {}
    for mentions in my_data['mentions']:
        for mention in mentions:
            mentions_count[mention] = mentions_count.get(mention, 0) + 1

    # Créer un DataFrame avec les comptes de mentions
    df_mentions = pd.DataFrame.from_dict(mentions_count, orient='index', columns=['count'])

    # Trier les mentions par ordre décroissant de nombre de comptes
    df_mentions = df_mentions.sort_values('count', ascending=False)

    # Créer un diagramme à barres pour les 10 premières mentions
    fig, ax = plt.subplots()
    ax.bar(df_mentions.index[:5], df_mentions['count'][:5])
    ax.set_xlabel('Mentions')
    ax.set_ylabel('Nombre de mentions')
    ax.set_title('Mentions les plus fréquentes')
    # Configurer l'axe des x
    ax.set_xticklabels(df_mentions.index, rotation=45, ha='right')
    st.pyplot(fig)

    # Fonction pour nettoyer le texte
    def clean_text(text):
        # Supprimer les caractères spéciaux
        text = re.sub(r'[^\w\s]', '', text)
        # Convertir en minuscules
        text = text.lower()
        return text

    # Nettoyage des tweets
    clean_tweets = my_data['text'].apply(clean_text)

    # Tokenization des tweets nettoyés
    words = []
    for tweet in clean_tweets:
        words += word_tokenize(tweet)

    # Comptage des mots
    word_counts = Counter(words)
    st.write("")
    # Affichage des 10 mots les plus fréquents
    st.markdown("#### Les 10 mots les plus fréquents dans les tweets (Sans les caractères spéciaux) : ")
    df_word_counts = pd.DataFrame(word_counts.most_common(10), columns=['mot', 'compte'])
    st.write(df_word_counts)
    st.write("")
    # Affichage d'un graphique
    fig, ax = plt.subplots()
    ax.bar(df_word_counts['mot'], df_word_counts['compte'])
    plt.xticks(rotation=45, ha='right')
    ax.set_title('Les 10 mots les plus fréquents')
    st.pyplot(fig)


