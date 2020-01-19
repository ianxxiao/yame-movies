import numpy as np


def get_min_max_year(year):
    return [int(year.min()), int(year.max())]


def get_genre_set(genres):
    genre_list = []

    # Add individual genre value to to genre list
    for item in genres:
        item = str(item).split("|")
        for i in item:
            genre_list.append(i)

    return np.unique(genre_list)


def isin_genres(df, selected_genres):
    # filter dataframe if there is user input criteria; default to 1 if not.

    if selected_genres:
        df = df.apply(lambda x: 1 if (set(x) >= selected_genres) else 0)
    else:
        df = 1

    return df