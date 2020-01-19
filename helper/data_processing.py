import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from helper.config import MINI_DATASET_URL
from youtube_search import YoutubeSearch
from time import sleep
from random import randint
import streamlit as st
import logging


@st.cache(persist=True)
def load_data():

    final_movie_df = pd.read_csv("./data/final_movie_df.csv")
    final_rating_df = pd.read_csv("./data/final_rating_df.csv")

    return final_movie_df, final_rating_df


def get_data(return_all=False, sample_frac=1.0):

    """
    This is the one time batch process to download data, clean, and look up YouTube links.
    Return:
        final_movie_df: a dataframe with all details for a movie
        final_movie_rating_df: a dataframe with user_level movie rating
    """

    # Create directory and downlaod data if not exist
    if not os.path.isfile('./data/mini_dataset.zip'):
        logging.info(f'Set up data directory ...')
        os.mkdir('./data')
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')

    # Load data to pandas
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))
    logging.info(f'complete raw data load ...')

    # Process individual datasets
    p_links, p_movies, p_rating = process_data(links, movies, ratings)

    # Create Analytical datasets
    movie_rating_avg_cnt = calc_movie_rating_average(p_movies, p_rating)

    # Create Final dataset
    final_movie_df = p_movies.copy().merge(movie_rating_avg_cnt.copy(),
                                           on='movieId', how='left').sample(frac=sample_frac)

    logging.info(f"start YouTube link search ...")
    final_movie_df['youtube_url'] = final_movie_df['title'].apply(lambda x: get_youtube_url(x))

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


def get_youtube_url(title):

    sleep(randint(1, 5)/10)
    logging.info(f"searching for: {title}")
    search_term = title + "trailer"
    results = YoutubeSearch(search_term, max_results=1).to_dict()

    if results:
        return 'https://www.youtube.com' + results[0]['link']

    else:
        logging.info(f"can't find link for {title}")
        return None


def cast_int(value):
    try:
        value = int(value)
    except ValueError:
        value = None
    return value


def make_clickable(title):
    search_str = 'http://www.google.com'
    return f'<a href="{search_str}">{title}</a>'
