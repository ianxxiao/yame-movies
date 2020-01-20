import streamlit as st
from helper.lookup import isin_genres
from datetime import date


def select_data(final_movie_df, add_year_selector, add_genre_selector, exploration=0):

    try:
        data = final_movie_df.loc[(final_movie_df['year'] >= add_year_selector[0]) &
                                  (final_movie_df['year'] <= add_year_selector[1]) &
                                  (isin_genres(final_movie_df['genres_set'], set(add_genre_selector)))] \
            .sample(5, random_state=int(str(date.today()).replace('-', ''))+exploration) \
            .sort_values("year", ascending=False) \
            .reset_index()

    except ValueError:
        st.text("Hmm. Can't find any movie based on your choice. Here are something else you may like.")
        data = final_movie_df.sample(random_state=int(str(date.today()).replace('-', ''))+exploration)

    # Show data
    try:
        st.table(data[['title', 'genres']])

    except ValueError:
        st.write(f"Not enough results. Here are all.")
        st.table(data[['title', 'genres']])

    return data