import streamlit as st
import time
import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt


from gensim import corpora
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from gensim.models.tfidfmodel import TfidfModel
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF


st.set_page_config(
    page_title="LDA/NMF", 
    page_icon="📈"
)

st.sidebar.header("Choose a demo")

# Créer un menu principal
menu = ['LDA','NMF']
# Ajouter les menus à la sidebar
choix = st.sidebar.selectbox('', menu)

df = st.session_state['data_clean']

# Si l'utilisateur choisit "Page 1", afficher le sous-menu
if choix == 'LDA':
    st.markdown("# Allocation de Dirichlet latente (LDA)")
    st.write('Dans cette partie nous entrainerons le modèle LDA.')
    st.subheader("Utiliser le modèle")
    traitements_checkbox = st.checkbox("Allocation de Dirichlet latente (LDA)")

    if traitements_checkbox:
        
        random.seed()

        # Diviser chaque tweet en une liste de mots séparés par des espaces
        preprocessed_docs = df['text_clean'].apply(lambda x: x.split())

        # Création d'un dictionnaire à partir des documents prétraités
        id2word = corpora.Dictionary(preprocessed_docs)

        # Transformation de chaque document en un vecteur de fréquence de mots
        corpus = [id2word.doc2bow(doc) for doc in preprocessed_docs]

        # Calcul de TF-IDF
        tfidf = TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        # Entraînement du modèle LDA
        lda_model = LdaModel(corpus=corpus_tfidf, id2word=id2word, num_topics=15, passes=25, random_state=100)

        # # Affichage des sujets avec leurs mots clés
        # topics = lda_model.print_topics(num_words=10)
        # for topic in topics:
        #      st.write(topic)

        st.write("")
        num_topics = 15
        # Affichage des sujets extraits
        topics = lda_model.show_topics(num_topics=15, formatted=False)
        for topic in topics:
            st.write("Topic {}: {}".format(topic[0], [word[0] for word in topic[1]]))

        # Calcul du score de cohérence
        coherence_model_lda = CoherenceModel(model=lda_model, texts=preprocessed_docs, dictionary=id2word, coherence='c_v')
        coherence_lda = coherence_model_lda.get_coherence()
        st.markdown("\n\n#### Coherence Score : " + str(coherence_lda))
        #st.write("\nCoherence Score: ", coherence_lda)

        #Affichage de la coherence/perpléxité

        perplexity = lda_model.log_perplexity(corpus)
        #st.write("\nPerplexité : ", perplexity)
        st.markdown("\n\n#### Perplexité : " + str(perplexity))


        st.markdown("\n\n#### Attribution des sujets aux 10 premiers documents")

        # Appliquer le modèle LDA aux 10 premiers documents
        for i in range(10):
            document = corpus[i]  # Obtenir le document i du corpus
            topics = lda_model.get_document_topics(document)  # Obtenir la distribution des sujets pour le document
            st.write(f"Document {i + 1}:")
            for topic in topics:
                st.write(f"Topic {topic[0]}: {topic[1]}")


        # Obtenir la distribution des sujets pour chaque document
        doc_topics = [lda_model.get_document_topics(doc) for doc in corpus]

        # Compter la fréquence de chaque sujet
        topic_freq = np.zeros(num_topics)
        for doc in doc_topics:
            for topic in doc:
                topic_freq[topic[0]] += 1

        # Afficher l'histogramme de la distribution des sujets
        plt.bar(range(num_topics), topic_freq)
        plt.xlabel("Sujet")
        plt.ylabel("Fréquence")
        plt.title("Distribution des sujets dans le corpus(Top 15)")
        st.pyplot(plt.show())


        # # Appliquer le modèle LDA aux documents
        # doc_topics = lda_model.get_document_topics(corpus)

        # # Afficher la distribution des sujets pour chaque document
        # for i, topics in enumerate(doc_topics):
        #     st.write(f"Document {i+1}:")
        #     for topic, prob in topics:
        #         st.write(f"Topic {topic}: {prob}")
        #     #print()

        
        # from wordcloud import WordCloud
        # 

        # # Pour chaque sujet
        # for topic_id in range(num_topics):
        #     words = lda_model.show_topic(topic_id, topn=10)  # Obtenir les mots clés du sujet
        #     topic_words = {word: score for word, score in words}
        #     wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(topic_words)
            
        #     # Afficher le nuage de mots du sujet
        #     plt.figure(figsize=(10, 5))
        #     plt.imshow(wordcloud, interpolation="bilinear")
        #     plt.axis("off")
        #     plt.title(f"Topic {topic_id}")
        #     st.pyplot(plt.show())


else:
    st.markdown("# Factorisation matricielle non négative (NMF)")
    st.write('Dans cette partie nous entrainerons le modèle NMF.')
    st.subheader("Utiliser le modèle")
    nmf_checkbox = st.checkbox("Factorisation matricielle non négative (NMF)")

    if nmf_checkbox:
        # Vectorisation des données
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)
        tfidf = tfidf_vectorizer.fit_transform(df['text_clean'])

        # Entraînement du modèle NMF
        nmf_model = NMF(n_components=10, random_state=42)
        nmf_model.fit(tfidf)

        # Analyse des sujets
        feature_names = tfidf_vectorizer.get_feature_names_out()
        for topic_idx, topic in enumerate(nmf_model.components_):
            topic_keywords = [feature_names[i] for i in topic.argsort()[:-11:-1]]
            topic_keywords_str = ", ".join(topic_keywords)
            #st.write("Topic #{topic_idx}: {topic_keywords_str}")
            st.write(f"Topic #{topic_idx}: {topic_keywords_str}")




