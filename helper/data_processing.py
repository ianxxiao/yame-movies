
def cast_int(value):
    try:
        value = int(value)
    except ValueError:
        value = None
    return value


def make_clickable(title):
    search_str = 'http://www.google.com'
    return f'<a href="{search_str}">{title}</a>'


def process_data(links, movies, ratings):

    # Process Movie Data
    movies['year'] = movies['title'].apply(lambda x: x.split('(')[-1]
                                           .strip(' )')).apply(lambda x: cast_int(x))
    movies['genres'] = movies['genres'].replace("(no genres listed)", None)
    movies['genres_set'] = movies['genres'].apply(lambda x: set(x.split("|")))
    movies['clickable_title'] = movies['title'].apply(lambda x: make_clickable(x))

    return links, movies, ratings


def join_data(movie, rating):

    movie_rating = movie.merge(rating, on='movieId', how='left')

    return movie_rating


def calc_movie_rating_average(movie, rating):

    movie_rating = join_data(movie, rating)

    avg_movie_rating = movie_rating.groupby("movieId")['rating'].agg(['mean', 'count'])

    avg_movie_rating.reset_index(inplace=True)
    avg_movie_rating.columns = ['movieId', 'avg_rating', 'review_cnt']

    return avg_movie_rating