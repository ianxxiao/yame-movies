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
    st.title("Yet Another Movie Recommender")
    exploration = st.slider("Exploration", 0.0, 1.0, step=0.1)
    links, movies, ratings = get_data()
    st.dataframe(links.head())
    st.dataframe(movies.head())
    st.dataframe(ratings.head())


if __name__ == '__main__':
    main()
