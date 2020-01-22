import sys
sys.path.append('../streamlit-recommendation')
import pytest
from helper import data_processing
from helper import lookup
from helper.recommendation import get_recomendation
import streamlit as st


def test_data():

    # clear streamlit cache because load_data uses cache decorator
    from streamlit import caching
    caching.clear_cache()

    df1, df2 = data_processing.load_data()

    assert df1.shape[0] > 0
    assert df1.shape[1] > 0
    assert df1[df1['youtube_url'].isna()].shape[0] == 0
    assert df2.shape[0] > 0
    assert df2.shape[1] > 0


final_movie_df, final_rating_df = data_processing.load_data()


@pytest.mark.parametrize("df", [final_movie_df])
def test_random_selection(df):
    for i in range(10):
        data = df.sample(10)
        link = data['youtube_url'].values[0]
        assert data.shape[0] == 10
        assert st.video(link)


@pytest.mark.parametrize("df, selected_genres", [(final_movie_df['genres'], 'Documentary'),
                                                 (final_movie_df['genres'], 'Drama')])
def test_genre_filtering(df, selected_genres):

    results = lookup.isin_genres(df, set(selected_genres))
    assert results.sum() > 0


@pytest.mark.parametrize("df, selected_years", [(final_movie_df, [1904, 1998]),
                                                 (final_movie_df, [2001, 2008])])
def test_year_filtering(df, selected_years):

    df = df.loc[(df['year'] >= selected_years[0]) & (final_movie_df['year'] <= selected_years[1])]

    assert df.shape[0] > 0


@pytest.mark.parametrize("df, selected_years", [(final_movie_df, 0),
                                                 (final_movie_df, 10)])
def test_recommendation(df, exploration):
    data = df.sample(10)
    data = get_recomendation(data, final_movie_df, exploration)
    link = data['youtube_url'].values[0]
    assert st.video(link)