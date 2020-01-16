import streamlit as st
import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from functions.recommendation import find_recommendation
from config import MINI_DATASET_URL


def cast_int(value):
    try:
        value = int(value)
    except ValueError:
        value = None
    return value


def process_data(links, movies, ratings):
    movies['year'] = movies['title'].apply(lambda x: x.split('(')[-1]
                                           .strip(' )')).apply(lambda x: cast_int(x))

    return links, movies, ratings


@st.cache
def get_data():
    if not os.path.isfile('./data/mini_dataset.zip'):
        os.mkdir('./data')
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))

    links, movies, ratings = process_data(links, movies, ratings)

    return links, movies, ratings


@st.cache
def get_min_max_year(year):

    return [int(year.min()), int(year.max())]


@st.cache
def get_genre_set(genres):

    return tuple(set(genres.unique()))


def main():

    # Load Data
    links, movies, ratings = get_data()

    # Set Up the Layout
    st.title("Yet Another Movie Recommender")

    add_selectbox = st.sidebar.selectbox("Number of Movie to Show",
                                         (5, 10, 20))

    add_year_selector = st.sidebar.slider(min_value=get_min_max_year(movies.year)[0],
                                          max_value=get_min_max_year(movies.year)[1],
                                          value=(get_min_max_year(movies.year)[0] + 20,
                                                 get_min_max_year(movies.year)[1] - 20),
                                          step=1, label="Select Year Range")

    add_genre_selector = st.sidebar.multiselect(label="select the Genre",
                                                options=get_genre_set(movies.genres))

    # Display Data
    st.subheader(f"Here are {add_selectbox} movies between {add_year_selector[0]} and {add_year_selector[1]}")
    st.table(movies[["title", "genres"]].loc[(movies['year'] >= add_year_selector[0]) &
                                             (movies['year'] <= add_year_selector[1])].sample(int(add_selectbox)))


if __name__ == '__main__':
    main()
