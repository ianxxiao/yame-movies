import streamlit as st

from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message, show_panel, \
    show_personalized_section, show_trailers
from helper.data_processing import load_data
from helper.select_data import select_data
from helper import recommendation
import pandas as pd
from helper.show_message import show_trailers

def main():

    # Load Data
    st.header("show some data")
    final_movie_df, final_rating_df = load_data()
    data = final_movie_df.sample(3)
    st.dataframe(data)
    st.dataframe(final_rating_df.sample(3))
    st.button('show something else.')

    st.dataframe(final_rating_df[final_rating_df['movieId']==4144])
    st.dataframe(final_movie_df[final_movie_df['movieId'] == 4144])

if __name__ == '__main__':
    main()