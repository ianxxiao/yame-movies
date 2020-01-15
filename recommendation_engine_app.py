import streamlit as st
import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from functions.recommendation import find_recommendation
from config import MINI_DATASET_URL


@st.cache
def get_data():
    if not os.path.isfile('./data/mini_dataset.zip'):
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))

    return links, movies, ratings


def main():
    links, movies, ratings = get_data()

    st.title("Yet Another Movie Recommender")

    st.subheader("Which movies do you like?")
    moive_1 = st.checkbox(movies['title'].sample(n=1).values[0], key=1)
    moive_2 = st.checkbox(movies['title'].sample(n=1).values[0], key=2)
    moive_3 = st.checkbox(movies['title'].sample(n=1).values[0], key=3)
    moive_4 = st.checkbox(movies['title'].sample(n=1).values[0], key=4)
    moive_5 = st.checkbox(movies['title'].sample(n=1).values[0], key=5)

    st.subheader("How adventurous do you feel today?")
    exploration = st.slider("2 means you want something unexpected", min_value=0.0, max_value=2.0, step=0.1)

    st.subheader("I think you may like these movies ...")
    reco_moive_1 = st.text(movies['title'].sample(n=1).values[0])
    reco_moive_2 = st.text(movies['title'].sample(n=1).values[0])
    reco_moive_3 = st.text(movies['title'].sample(n=1).values[0])
    reco_moive_4 = st.text(movies['title'].sample(n=1).values[0])
    reco_moive_5 = st.text(movies['title'].sample(n=1).values[0])

if __name__ == '__main__':
    main()
