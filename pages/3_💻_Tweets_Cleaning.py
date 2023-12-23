import streamlit as st
import nltk
import time
import numpy as np
import pandas as pd
import re
import string
import wordcloud
import io
import requests
import PIL
import matplotlib.pyplot as plt


nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('omw-1.4')

#nltk.download('francais')


from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
from wordcloud import WordCloud

st.set_page_config(
    page_title="Tweets Cleaning", 
    page_icon="💻"
)

st.set_option('deprecation.showPyplotGlobalUse', False)

if 'data_clean' not in st.session_state:
    st.session_state['data_clean'] = ''

if 'cleanUp' not in st.session_state:
    st.session_state['cleanUp'] = ''

my_data = pd.DataFrame() # initialisation de la variable df

#Methodes
#Suppression liens
def remove_links(text):
    text = re.sub(r'http\S+', '', text)
    return text

#clean_hashtags   
def clean_hashtags(text):
    hashtags = re.findall(r'#\w+', text)
    for hashtag in hashtags:
        cleaned_hashtag = re.sub(r'[^\w]+', '', hashtag)
        text = text.replace(hashtag, cleaned_hashtag)
    return text


#Suppression hashtags
def remove_hashtags(text):
    #text = re.sub(r'#(\w+)', '', text)
    text = re.sub(r'#\w+', '', text)
    return text

#Suppression mentions
def remove_mentions(text):
    text = re.sub(r'@(\w+)', '', text)
    return text               

#Suppression emojis
def remove_emojis(text):
    text = re.sub(r'[^\w\s#@/:%.,_-]', '', text, flags=re.UNICODE)
    #text = text.encode('ascii', 'ignore').decode('ascii')
    return text

# #Suppression ponctuations
# def remove_ponc(text):
#     text = text.translate(str.maketrans("", "", string.punctuation))
#     text = " ".join(text.split())
#     return text

#Suppression caractères spéciaux
def remove_special_chars(text):
    #text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'[^\w\s]|_', '', text)
    return text            


img = "https://raw.githubusercontent.com/linogaliana/python-datascientist/master/content/course/NLP/book.png"
book_mask = np.array(PIL.Image.open(io.BytesIO(requests.get(img).content)))

def make_wordcloud(corpus):
    wc = wordcloud.WordCloud(background_color="white", max_words=200, mask=book_mask, contour_width=3, contour_color='steelblue')
    wc.generate(corpus)
    return wc


def essai(data, remove_links_checkbox,remove_hashtags_checkbox,remove_mentions_checkbox,remove_emojis_checkbox,
remove_special_chars_checkbox):

    my_data['text_clean'] = my_data['text']

    if remove_links_checkbox:
        my_data['text_clean'] = my_data['text_clean'].apply(remove_links)

    if remove_hashtags_checkbox:
        my_data['text_clean'] = my_data['text_clean'].apply(remove_hashtags)
        #my_data['text_clean'] = my_data['text_clean'].apply(lambda x: clean_hashtags(x))

    if remove_mentions_checkbox:
        my_data['text_clean'] = my_data['text_clean'].apply(remove_mentions)

    if remove_emojis_checkbox:
        my_data['text_clean'] = my_data['text_clean'].apply(remove_emojis)

    if remove_special_chars_checkbox:
        my_data['text_clean'] = my_data['text_clean'].apply(remove_special_chars)
    
    # if remove_ponc_checkbox:
    #     my_data['text_clean'] = my_data['text_clean'].apply(remove_ponc)

    return my_data


# Fonction pour effectuer la tokenization, la suppression des stop-words, Stemming, lemmatization
 # Chargement des stop-words en français
stop_words = stopwords.words('french')

# Initialisation du lemmatiseur
lemmatizer = WordNetLemmatizer()

#stemming
stemmer = SnowballStemmer(language='french')

def preprocess_text(text):
    # Conversion en minuscules
    text = text.lower()
    # Tokenization
    tokens = word_tokenize(text, language='french')
    # Suppression des caractères spéciaux et de la ponctuation
    tokens = [word for word in tokens if word.isalpha()]
    # Suppression des stop-words
    tokens = [word for word in tokens if word not in stop_words]
    # Stemmatisation
    stemmed = [stemmer.stem(word) for word in tokens]
    # Lemmatisation
    tokens = [lemmatizer.lemmatize(word) for word in tokens]
    # Reconstitution du texte à partir des tokens
    text = ' '.join(tokens)
    return text

st.markdown("# Tweets Cleaning")

st.write(
"""
Dans cette partie nous utiliserons des méthodes de nettoyage de tweets.
La suppression des caractères spéciaux, des ponctuations, des émojis, des liens, des hashtags 
et mentions dans le texte des tweets. 
La stemmatisation, la lemmatisation et tokenisation.

"""
)
st.sidebar.header("Choose a demo")

# Créer un menu principal
menu = ['Upload','Preprocessing', 'Word Processor']
# Ajouter les menus à la sidebar
choix = st.sidebar.selectbox('', menu)

#Upload le fichier
# uploaded_file = st.file_uploader("Choisissez un fichier CSV", type="csv")

# if uploaded_file is not None:
#     # Stockage de la variable globale
#     my_data = load_csv(uploaded_file) 
#     st.session_state['my_data_glob'] = my_data   
#     my_data['text_clean'] =''

my_data = st.session_state['my_data_glob']
#my_data['text_clean'] =''

if not my_data.empty:

    # Choix l'utilisateur
    if choix == 'Preprocessing':
        st.subheader("Options de nettoyage")
        remove_links_checkbox = st.checkbox("Supprimer les liens")
        remove_special_chars_checkbox = st.checkbox("Supprimer les caractères spéciaux")
        # remove_ponc_checkbox = st.checkbox("Supprimer les des ponctuations")
        remove_emojis_checkbox = st.checkbox("Supprimer les émojis")
        remove_hashtags_checkbox = st.checkbox("Supprimer les hashtags")
        remove_mentions_checkbox = st.checkbox("Supprimer les mentions")

        st.session_state['data_clean'] = essai(my_data, remove_links_checkbox,remove_hashtags_checkbox,remove_hashtags_checkbox,remove_emojis_checkbox,
remove_special_chars_checkbox)

        dataclean = st.session_state['data_clean']
        st.session_state['cleanUp'] = dataclean
        #if upload:
            # Afficher un bouton de téléchargement
        if remove_links_checkbox or remove_hashtags_checkbox or remove_mentions_checkbox or remove_special_chars_checkbox:
            st.write("")
            st.write("")
            st.markdown('### Téléchargement du fichier prétraité')
            st.download_button(
                label="Télécharger les données (CSV)",
                data=my_data.to_csv().encode("utf-8"),
                file_name="votre_fichier.csv",
                mime="text/csv",
            )
            st.write("")
            df_selected = dataclean[['text', 'text_clean']].head(5)
            st.dataframe(df_selected, use_container_width=False)      

    if choix == 'Word Processor':
        a =  st.session_state['cleanUp']
        st.markdown("### WordCloud avant Stemming/Lemmatization/Supp StopWords")
       
        words_list = a['text_clean'].unique().tolist()
        pos_words = " ".join(words_list)

        fig = plt.figure()
       # plt.imshow(make_wordcloud(' '.join(a['text_clean'])))
        plt.imshow(make_wordcloud(pos_words))
        plt.axis("off")
        st.pyplot(fig)
        #plt.savefig('word.png', bbox_inches='tight')

        #Stemming/Lemmatization/Supp StopWords
        st.subheader("Options de nettoyage")
        traitements_checkbox = st.checkbox("Tokenization/Stop-Words/Stemming/Lemmatization")
        

        if traitements_checkbox:
            a['text_clean'] = a['text_clean'].apply(preprocess_text)
    
            st.write("")
            st.write("")
            st.markdown('### Téléchargement du fichier traité')
            st.download_button(
                label="Télécharger les données (CSV)",
                data=my_data.to_csv().encode("utf-8"),
                file_name="votre_fichier_traite.csv",
                mime="text/csv",
            )
            #selected_columns = ['text', 'text_clean']

            st.write("")
            #st.write(a[selected_columns].head())
            df_selected = a[['text', 'text_clean']].head(5)
            st.dataframe(df_selected, use_container_width=True)

            #Apres Stemming
            st.markdown("### WordCloud après Stemming/Lemmatization/Supp StopWords")
       
            st.write("")
            wordslist = a['text_clean'].unique().tolist()
            poswords = " ".join(wordslist)
            # wc = make_wordcloud(poswords)
            # fig = plt.figure()
            # plt.imshow(wc, interpolation='bilinear')
            # plt.axis("off")
            # st.pyplot(fig)
            # On peut ajuster les stop words
            my_stop_words = stop_words
            my_stop_words.extend(['si', 'non', 'toujours', 'cette', 'ca', 'après', 'très', 'plus', 'cest', 'a', 'contre'])

            neg_wordcloud =  WordCloud(
                            width=800, height = 500,            
                            stopwords=my_stop_words).generate(poswords)

            plt.figure(figsize=(8, 8), facecolor = None)
            plt.imshow(neg_wordcloud)
            plt.axis("off")
            plt.tight_layout(pad=0)
            st.pyplot(plt.show())

    elif choix == 'Upload':
        #if uploaded_file is not None:
        # Afficher le DataFrame et ajouter une barre de recherche
        search_term = st.text_input('Recherche', '')
        filtered_df = my_data[my_data['text'].str.contains(search_term, case=False)]
        st.dataframe(filtered_df.head())

       # st.write(my_data.head())
