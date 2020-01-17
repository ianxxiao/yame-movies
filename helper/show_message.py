import streamlit as st
from PIL import Image

def show_header_message():
    if st.button("Click to know more about YAME"):
        st.markdown("YAME means **Y**et **A**nother **M**ovie **E**xplorer. \
                     Algorithms on sites like YouTube or Netflix suck! \
                     They create an echo chamber. \
                     They make you watch the same boring videos, over and over. :zzz:"
                    )
        st.markdown("Instead, YAME's algorithm takes you on a journey. YAME makes entertainment exciting, again. :fire:")
        st.markdown("Click the arrow on the left to refine your suggestions :arrow_forward:")
        st.markdown("**Like YAME?** \
                    [Sign up](https://docs.google.com/forms/d/e/1FAIpQLSf9bL0StMXnjjfSlhgekbMFJNw5okT2bpFUqfO-O8dAbPfKCw/viewform?usp=sf_link) to receive weekly suggestions. \
                     Follow us on [Instagram](https://www.instagram.com/yame_movies/). \
                     Save YAME to your phone so you can use it anytime like any other app. :iphone:")

        image = Image.open("./asset/save_to_phone.jpeg")
        st.image(image)

        st.markdown("_YAME is built by Ian Xiao. \
                     You can find him on [LinkedIn](https://www.linkedin.com/in/ianxiao/), \
                     [Medium](https://medium.com/@ianxiao), \
                     and [Twitter](https://twitter.com/ian_xxiao)._")


def show_foot_message():

    st.markdown("* * *")
    st.markdown("**Like YAME?** \
                [Sign up](https://docs.google.com/forms/d/e/1FAIpQLSf9bL0StMXnjjfSlhgekbMFJNw5okT2bpFUqfO-O8dAbPfKCw/viewform?usp=sf_link) to receive weekly suggestions. \
                Follow us on [Instagram](https://www.instagram.com/yame_movies/). Save YAME to your phone. :iphone:")
    st.markdown("_YAME is built by Ian Xiao. \
                You can find him on [LinkedIn](https://www.linkedin.com/in/ianxiao/), \
                [Medium](https://medium.com/@ianxiao), \
                and [Twitter](https://twitter.com/ian_xxiao)._")