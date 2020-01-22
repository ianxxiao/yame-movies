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
                  min_value=0, max_value=10, value=5, step=1)

    # set up recommender
    recommender = recommendation.KnnRecommender(['The Imitation Game (2014)',
                                                 'Shutter Island (2010)'], exploration)
    recommender.make_recommendations(11)
    st.dataframe(recommender.get_recommendations())


if __name__ == '__main__':
    main()