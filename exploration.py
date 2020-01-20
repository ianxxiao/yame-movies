import streamlit as st

from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message, show_panel, \
    show_personalized_section, show_trailers
from helper.data_processing import load_data
from helper.select_data import select_data


def main():

    # Load Data

    final_movie_df, final_rating_df = load_data()
    st.dataframe(final_movie_df.sample(10))
    st.text(final_movie_df[final_movie_df['youtube_url'].isna()].shape)
    st.button('show something else.')


if __name__ == '__main__':
    main()