import sys
sys.path.append('../streamlit-recommendation')
import pytest
from helper import data_processing
from helper import lookup


def test_data():

    final_movie_df, final_rating_df = data_processing.load_data()

    assert final_movie_df.shape[0] > 0
    assert final_movie_df.shape[1] > 0
    assert final_rating_df.shape[0] > 0
    assert final_rating_df.shape[1] > 0


final_movie_df, final_rating_df = data_processing.load_data()


@pytest.mark.parametrize("df, selected_genres", [(final_movie_df['genres'], 'Documentary'),
                                                 (final_movie_df['genres'], 'Drama')])
def test_genre_filtering(df, selected_genres):

    results = lookup.isin_genres(df, set(selected_genres))
    assert results.sum() > 0


@pytest.mark.parametrize("df, selected_years", [(final_movie_df, [1904, 1998]),
                                                 (final_movie_df, [2001, 2008])])
def test_year_filtering(df, selected_years):

    final_movie_df.loc[(df['year'] >= selected_years[0]) & (final_movie_df['year'] <= selected_years[1])]

    assert final_movie_df.shape[0] > 0