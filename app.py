import streamlit as st
import pandas as pd
from zipfile import ZipFile
import urllib.request, os
from config import MINI_DATASET_URL
from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message
from helper.data_processing import process_data
from helper.lookup import get_min_max_year, get_genre_set, isin_genres


# Persist to disk so the web-app doesn't re-load when a user refresh the browser
@st.cache(persist=True)
def get_data():

    # Create directory and downlaod data if not exist
    if not os.path.isfile('./data/mini_dataset.zip'):
        os.mkdir('./data')
        urllib.request.urlretrieve(MINI_DATASET_URL, './data/mini_dataset.zip')

    # Load data to pandas
    links = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/links.csv'))
    movies = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/movies.csv'))
    ratings = pd.read_csv(ZipFile('./data/mini_dataset.zip').open('ml-latest-small/ratings.csv'))

    return links, movies, ratings


def main():
    # Load Data
    links, movies, ratings = get_data()
    p_links, p_movies, p_rating = process_data(links.copy(), movies.copy(), ratings.copy())

    # Set Up the Layout
    st.title("Yet Another Movie Explorer")
    show_header_message()

    add_year_selector = st.sidebar.slider(label="Pick the Year",
                                          min_value=get_min_max_year(p_movies.year)[0],
                                          max_value=get_min_max_year(p_movies.year)[1],
                                          value=(get_min_max_year(p_movies.year)[1] - 20,
                                                 get_min_max_year(p_movies.year)[1]),
                                          step=1)

    add_genre_selector = st.sidebar.multiselect(label="Pick the Genre (default to any)",
                                                options=get_genre_set(p_movies.genres))

    st.markdown("* * *")
    st.subheader(f"5 Movies from {add_year_selector[0]} to {add_year_selector[1]}. Just for You.")

    # Filter data
    try:
        data = p_movies.loc[(p_movies['year'] >= add_year_selector[0]) &
                            (p_movies['year'] <= add_year_selector[1]) &
                            (isin_genres(p_movies['genres_set'], set(add_genre_selector)))] \
            .sample(5) \
            .sort_values("year", ascending=False) \
            .reset_index()

    except ValueError:
        st.text("Hmm. Can't find any movie based on your choice. Here are something else you may like.")
        data = p_movies.sample(5)

    # Show data
    try:
        st.table(data[['title', 'genres']])

    except ValueError:
        st.write(f"Not enough results. Here are all.")
        st.table(data[['title', 'genres']])

    st.button("Meh. Show Me Something Else.", key=1)

    # Get Youtube Trailers
    for title in data['title']:
        search_term = title + "trailer"
        results = YoutubeSearch(search_term, max_results=1).to_dict()
        try:
            st.subheader(title)
            st.video('https://www.youtube.com' + results[0]['link'])

        except IndexError:
            st.text(f"Hm. We can't find any tailor for {title}. Click button below to find something else.")

    st.button("Meh. Show Me Something Else.", key=2)

    show_foot_message()


if __name__ == '__main__':
    main()
