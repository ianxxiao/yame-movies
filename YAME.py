import streamlit as st

from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message, show_panel, \
    show_personalized_section, show_trailers
from helper.data_processing import load_data
from helper.select_data import select_data
from helper.recommendation import get_recomendation
import logging

def main():
    # Load Data
    final_movie_df, final_rating_df = load_data()
    max_rating = final_rating_df['rating'].max()

    # Set Up the Layout
    st.title("Yet Another Movie Explorer")
    show_header_message()
    add_year_selector, add_genre_selector = show_panel(final_movie_df)

    # Today's Pick
    st.markdown("* * *")
    st.subheader(f"Today's Pick from {add_year_selector[0]} to {add_year_selector[1]}.")
    st.text(f"You can refine year and genre using the panel on the left.")

    data = select_data(final_movie_df, add_year_selector, add_genre_selector)
    show_trailers(data, max_rating)

    # Personalization Section
    exploration = show_personalized_section()
    try:
        data = get_recomendation(data, final_movie_df, final_rating_df, exploration)
        show_trailers(data, max_rating)
    except KeyError or IndexError:
        # fail safe solution
        logging.warning('SOMETHING WENT WRONG IN RECOMMENDATION. USE FAIL SAFE.')
        data = select_data(final_movie_df, add_year_selector, add_genre_selector)
        show_trailers(data, max_rating)

    # Foot Note
    show_foot_message()


if __name__ == '__main__':
    main()
