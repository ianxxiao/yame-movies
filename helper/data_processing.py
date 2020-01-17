
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
