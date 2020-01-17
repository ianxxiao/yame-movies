import streamlit as st
from PIL import Image
from helper.config import IG_URL, GOOGLE_FORM_URL

def show_header_message():
    if st.button("Click to know more about YAME"):
        st.markdown("YAME means **Y**et **A**nother **M**ovie **E**xplorer. \
                     Algorithms on sites like YouTube or Netflix suck! \
                     They create an echo chamber. \
                     They make you watch the same boring videos, over and over. :zzz:"
                    )
        st.markdown("Instead, YAME's algorithm takes you on a journey. YAME makes entertainment exciting, again. :fire:")
        st.markdown("Click the arrow on the left to refine your suggestions :arrow_forward:")
        st.markdown(f"**Like YAME?** \
                    [Sign up]({GOOGLE_FORM_URL}) to receive weekly suggestions. \
                     Follow us on [Instagram]({IG_URL}). \
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
                Follow us on [Instagram]({IG_URL}). Save YAME to your phone. :iphone:")
    st.markdown("_YAME is built by Ian Xiao. \
                You can find him on [LinkedIn](https://www.linkedin.com/in/ianxiao/), \
                [Medium](https://medium.com/@ianxiao), \
                and [Twitter](https://twitter.com/ian_xxiao)._")