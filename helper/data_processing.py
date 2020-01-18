import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from helper.config import MINI_DATASET_URL
import streamlit as st


# Persist to disk so the web-app doesn't re-load when a user refresh the browser
@st.cache(persist=True)
def get_data(return_all=False):

    # Create directory and downlaod data if not exist
    if not os.path.isfile('./data/mini_dataset.zip'):
        os.mkdir('./data')
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')

    # Load data to pandas
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))

    # Process individual datasets
    p_links, p_movies, p_rating = process_data(links, movies, ratings)

    # Create Analytical datasets
    movie_rating_avg_cnt = calc_movie_rating_average(p_movies, p_rating)

    # Create Final dataset
    final_movie_df = p_movies.copy().merge(movie_rating_avg_cnt.copy(), on='movieId', how='left')

    if not return_all:
        return final_movie_df.copy(), p_rating.copy()
    else:
        return p_links.copy(), p_movies.copy(), p_rating.copy(), movie_rating_avg_cnt.copy()


def process_data(links, movies, ratings):

    # Process Movie Data
    movies['year'] = movies['title'].apply(lambda x: x.split('(')[-1]
                                           .strip(' )')).apply(lambda x: cast_int(x))
    movies['genres'] = movies['genres'].replace("(no genres listed)", None)
    movies['genres_set'] = movies['genres'].apply(lambda x: set(x.split("|")))
    movies['clickable_title'] = movies['title'].apply(lambda x: make_clickable(x))

    return links, movies, ratings


def calc_movie_rating_average(movie, rating):

    # need to use copy, otherwise it gives a cache warning
    movie_rating = movie.copy().merge(rating.copy(), on='movieId', how='left')

    avg_movie_rating = movie_rating.groupby("movieId")['rating'].agg(['mean', 'count'])

    avg_movie_rating.reset_index(inplace=True)
    avg_movie_rating.columns = ['movieId', 'avg_rating', 'review_cnt']

    return avg_movie_rating


def cast_int(value):
    try:
        value = int(value)
    except ValueError:
        value = None
    return value


def make_clickable(title):
    search_str = 'http://www.google.com'
    return f'<a href="{search_str}">{title}</a>'
