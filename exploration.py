import streamlit as st
import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from config import MINI_DATASET_URL
from helper.data_processing import process_data, join_data, calc_movie_rating_average


# Persist to disk so the web-app doesn't re-load when a user refresh the browser
@st.cache(persist=True, allow_output_mutation=False)
def get_data():

    # Create directory and downlaod data if not exist
    if not os.path.isfile('./data/mini_dataset.zip'):
        os.mkdir('./data')
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')

    # Load data to pandas
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))

    p_links, p_movies, p_rating = process_data(links.copy(), movies.copy(), ratings.copy())
    movie_rating_avg_cnt = calc_movie_rating_average(p_movies.copy(), p_rating.copy())

    return p_links, p_movies, p_rating, movie_rating_avg_cnt


def main():

    # Load Data
    p_links, p_movies, p_rating, movie_rating_avg_cnt = get_data()

    # display Data
    st.write("p_movies")
    st.dataframe(p_movies)

    st.write("p_links")
    st.dataframe(p_links)

    st.write("p_rating")
    st.dataframe(p_rating)

    st.write("movie_rating")
    movie_rating = join_data(p_movies, p_rating)
    st.dataframe(movie_rating)
    st.write(movie_rating.shape)
    st.write("unique movie id: " + str(len(movie_rating['movieId'].unique())))

    st.write("movie average rating and count")
    movie_rating_avg_cnt = calc_movie_rating_average(p_movies, p_rating)
    st.dataframe(movie_rating_avg_cnt)
    st.write(movie_rating_avg_cnt.shape)



if __name__ == '__main__':
    main()