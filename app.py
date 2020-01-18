import streamlit as st

from youtube_search import YoutubeSearch
from helper.show_message import show_header_message, show_foot_message
from helper.data_processing import get_data
from helper.lookup import get_min_max_year, get_genre_set, isin_genres


def main():

    # Load Data
    final_movie_df, final_rating_df = get_data()
    max_rating = final_rating_df['rating'].max()

    # Set Up the Layout
    st.title("Yet Another Movie Explorer")
    show_header_message()

    add_year_selector = st.sidebar.slider(label="Pick the Year",
                                          min_value=get_min_max_year(final_movie_df.year)[0],
                                          max_value=get_min_max_year(final_movie_df.year)[1],
                                          value=(get_min_max_year(final_movie_df.year)[1] - 20,
                                                 get_min_max_year(final_movie_df.year)[1]),
                                          step=1)

    add_genre_selector = st.sidebar.multiselect(label="Pick the Genre (default to any)",
                                                options=get_genre_set(final_movie_df.genres))

    st.markdown("* * *")
    st.subheader(f"5 Movies from {add_year_selector[0]} to {add_year_selector[1]}. Just for You.")

    # Filter data
    try:
        data = final_movie_df.loc[(final_movie_df['year'] >= add_year_selector[0]) &
                            (final_movie_df['year'] <= add_year_selector[1]) &
                            (isin_genres(final_movie_df['genres_set'], set(add_genre_selector)))] \
            .sample(5) \
            .sort_values("year", ascending=False) \
            .reset_index()

    except ValueError:
        st.text("Hmm. Can't find any movie based on your choice. Here are something else you may like.")
        data = final_movie_df.sample(5)

    # Show data
    try:
        st.table(data[['title', 'genres']])

    except ValueError:
        st.write(f"Not enough results. Here are all.")
        st.table(data[['title', 'genres']])

    st.button("Meh. Show Me Something Else.", key=1)
    st.markdown("***")

    # Get Youtube Trailers
    for title in data['title']:
        search_term = title + "trailer"
        results = YoutubeSearch(search_term, max_results=1).to_dict()
        try:
            st.subheader(title)
            st.video('https://www.youtube.com' + results[0]['link'])

            avg_rating = data[data.title == title]['avg_rating'].values[0]
            review_cnt = data[data.title == title]['review_cnt'].values[0]
            st.text(f"Average Score: {avg_rating: .1f} out of {max_rating}")
            st.text(f"Numbers of Reviews: {review_cnt}")

            st.markdown("***")

        except IndexError:
            st.text(f"Hm. We can't find any tailor for {title}. Click button below to find something else.")
            st.markdown("***")

    st.button("Meh. Show Me Something Else.", key=2)

    show_foot_message()


if __name__ == '__main__':
    main()