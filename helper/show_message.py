import streamlit as st
from PIL import Image
from helper.config import IG_URL, GOOGLE_FORM_URL
from helper.lookup import get_min_max_year, get_genre_set


def show_panel(final_movie_df):

    add_year_selector = st.sidebar.slider(label="Pick the Year",
                                          min_value=get_min_max_year(final_movie_df.year)[0],
                                          max_value=get_min_max_year(final_movie_df.year)[1],
                                          value=(get_min_max_year(final_movie_df.year)[1] - 20,
                                                 get_min_max_year(final_movie_df.year)[1]),
                                          step=1)

    add_genre_selector = st.sidebar.multiselect(label="Pick the Genre (default to any)",
                                                options=get_genre_set(final_movie_df.genres))

    return add_year_selector, add_genre_selector


def show_header_message():
    if st.button("Click to know more about YAME"):
        st.markdown("YAME means **Y**et **A**nother **M**ovie **E**xplorer. \
                     Algorithms on sites like YouTube or Netflix suck! \
                     They create chambers. \
                     They make you watch the same boring videos, over and over. :zzz:"
                    )
        st.markdown("Instead, YAME's algorithm takes you on a journey. YAME makes entertainment exciting, again. :fire:")
        st.markdown("Click the arrow on the left to refine your suggestions :arrow_forward:")
        st.markdown(f"**Like YAME?** \
                    [Sign up]({GOOGLE_FORM_URL}) to receive weekly suggestions. \
                     Follow us on [Instagram]({IG_URL}) to see great movie quotes. \
                     Save YAME to your phone so you can use it anytime like any other app. :iphone:")

        image = Image.open("./asset/save_to_phone.jpeg")
        st.image(image)

        st.markdown("_YAME is built by Ian Xiao. \
                     You can find him on [LinkedIn](https://www.linkedin.com/in/ianxiao/), \
                     [Medium](https://medium.com/@ianxiao), \
                     and [Twitter](https://twitter.com/ian_xxiao)._")


def show_foot_message():

    st.markdown("* * *")
    st.markdown(f"**Like YAME?** \
                  [Sign up]({GOOGLE_FORM_URL}) to receive weekly suggestions. \
                   Follow us on [Instagram]({IG_URL}) to see great movie quotes. \
                   Save YAME to your phone so you can use it anytime like any other app. :iphone:")
    st.markdown("_YAME is built by Ian Xiao. \
                You can find him on [LinkedIn](https://www.linkedin.com/in/ianxiao/), \
                [Medium](https://medium.com/@ianxiao), \
                and [Twitter](https://twitter.com/ian_xxiao)._")


def show_personalized_section():

    st.subheader(f'Your Personalized List.')
    exploration = st.slider(f'How adventurous would you like to be? '
                  f'(100 - show something totally different)',
                  min_value=0, max_value=100, value=50, step=10)
    return exploration


def show_trailers(data, max_rating):

    # Show Youtube Trailers
    for title in data['title']:

        st.subheader(title)
        link = data[data.title == title]['youtube_url'].values[0]
        avg_rating = data[data.title == title]['avg_rating'].values[0]
        review_cnt = data[data.title == title]['review_cnt'].values[0]

        if link != 'nan':
            st.video(link)
            st.text(f"Average Score: {avg_rating: .1f} out of {max_rating}")
            st.text(f"Numbers of Reviews: {review_cnt}")

        else:
            st.text(f"Hm. We can't find any tailor for {title}. Click button below to find something else.")

        st.markdown("***")