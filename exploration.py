import streamlit as st
import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from helper.config import MINI_DATASET_URL
from helper.data_processing import get_data


def main():

    # Load Data
    p_links, p_movies, p_rating, movie_rating_avg_cnt = get_data(return_all=True)

    st.dataframe(p_movies)
    st.text("Unique Movie ID: " + str(len(p_movies['movieId'].value_counts())))

    st.dataframe(p_rating)


if __name__ == '__main__':
    main()