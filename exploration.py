import streamlit as st

from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message, show_panel, \
    show_personalized_section, show_trailers
from helper.data_processing import load_data
from helper.select_data import select_data
from helper import recommendation
import pandas as pd

def main():

    # Load Data
    st.header("show some data")
    final_movie_df, final_rating_df = load_data()
    st.dataframe(final_movie_df.sample(3))
    st.dataframe(final_rating_df.sample(3))
    st.button('show something else.')

    # Slider
    st.header("prototype Smart Exploration")
    exploration = st.slider(f'How adventurous would you like to be? '
                  f'(100 - show something totally different)',
                  min_value=0, max_value=100, value=50, step=10)

    # set up recommender
    recommender = recommendation.KnnRecommender()
    reco = recommender.make_recommendations('The Imitation Game (2014)', 20)
    st.dataframe(reco)


if __name__ == '__main__':
    main()