import sys
sys.path.append('../streamlit-recommendation')
import os
import time
import gc
import argparse
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from fuzzywuzzy import fuzz
from helper import data_processing


def get_recomendation(movie_set, final_movie_df, final_rating_df, exploration):
    '''
    driver function to get recommendation based on a set of movies and user define exploration
    :return: a data frame of movie and youtube url
    '''

    recommender = KnnRecommender(movie_set['title'].tolist(), final_movie_df,
                                 final_rating_df, exploration)
    recommender.make_recommendations(11)
    data = recommender.return_recommendations()

    return data


class KnnRecommender():
    """
    This is an item-based collaborative filtering recommender with
    KNN implmented by sklearn
    """

    def __init__(self, movie_set, final_movie_df, final_rating_df, exploration):
        """
        Recommender requires path to data: movies data and ratings data
        Parameters
        ----------
        path_movies: str, movies data file path
        path_ratings: str, ratings data file path
        """
        self.movie_rating_thres = 0
        self.user_rating_thres = 0
        self.model = NearestNeighbors()
        self.set_filter_params(0, 0)
        self.set_model_params(20, 'brute', 'cosine', -1)
        self.recommendations = {}
        self.movie_set = movie_set
        self.exploration = exploration
        self.final_movie_df = final_movie_df
        self.final_rating_df = final_rating_df

    def set_filter_params(self, movie_rating_thres, user_rating_thres):
        """
        set rating frequency threshold to filter less-known movies and
        less active users
        Parameters
        ----------
        movie_rating_thres: int, minimum number of ratings received by users
        user_rating_thres: int, minimum number of ratings a user gives
        """
        self.movie_rating_thres = movie_rating_thres
        self.user_rating_thres = user_rating_thres

    def set_model_params(self, n_neighbors, algorithm, metric, n_jobs=None):
        """
        set model params for sklearn.neighbors.NearestNeighbors
        Parameters
        ----------
        n_neighbors: int, optional (default = 5)
        algorithm: {'auto', 'ball_tree', 'kd_tree', 'brute'}, optional
        metric: string or callable, default 'minkowski', or one of
            ['cityblock', 'cosine', 'euclidean', 'l1', 'l2', 'manhattan']
        n_jobs: int or None, optional (default=None)
        """
        if n_jobs and (n_jobs > 1 or n_jobs == -1):
            os.environ['JOBLIB_TEMP_FOLDER'] = '/tmp'
        self.model.set_params(**{
            'n_neighbors': n_neighbors,
            'algorithm': algorithm,
            'metric': metric,
            'n_jobs': n_jobs})

    def _prep_data(self):
        """
        prepare data for recommender
        1. movie-user scipy sparse matrix
        2. hashmap of movie to row index in movie-user scipy sparse matrix
        """
        # read data
        # df_movies, df_ratings = data_processing.load_data()
        df_movies = self.final_movie_df[['movieId', 'title']]
        df_ratings = self.final_rating_df[['userId', 'movieId', 'rating']]

        df_movies.astype({'movieId': 'int32', 'title': 'str'})

        df_ratings.astype({'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
        df_ratings = df_ratings[df_ratings['movieId'].isin(df_movies['movieId'].tolist())]

        df_movies_cnt = pd.DataFrame(
            df_ratings.groupby('movieId').size(),
            columns=['count'])
        popular_movies = list(set(df_movies_cnt.query('count >= @self.movie_rating_thres').index))  # noqa
        movies_filter = df_ratings.movieId.isin(popular_movies).values

        df_users_cnt = pd.DataFrame(
            df_ratings.groupby('userId').size(),
            columns=['count'])
        active_users = list(set(df_users_cnt.query('count >= @self.user_rating_thres').index))  # noqa
        users_filter = df_ratings.userId.isin(active_users).values

        df_ratings_filtered = df_ratings[movies_filter & users_filter]

        # pivot and create movie-user matrix
        movie_user_mat = df_ratings_filtered.pivot(
            index='movieId', columns='userId', values='rating').fillna(0)
        # create mapper from movie title to index
        hashmap = {
            movie: i for i, movie in
            enumerate(list(df_movies.set_index('movieId').loc[movie_user_mat.index].title))  # noqa
        }
        # transform matrix to scipy sparse matrix
        movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

        # clean up
        del df_movies, df_movies_cnt, df_users_cnt
        del df_ratings, df_ratings_filtered, movie_user_mat
        gc.collect()
        return movie_user_mat_sparse, hashmap

    def _idx_lookup(self, hashmap, fav_movie):

        if  hashmap.get(fav_movie):
            return hashmap.get(fav_movie)
        else:
            return hashmap.popitem()[1]


    def _fuzzy_matching(self, hashmap, fav_movie):
        """
        return the closest match via fuzzy ratio.
        If no match found, return None
        Parameters
        ----------
        hashmap: dict, map movie title name to index of the movie in data
        fav_movie: str, name of user input movie
        Return
        ------
        index of the closest match
        """
        match_tuple = []
        # get match
        for title, idx in hashmap.items():
            print(f"{title} : {type(title)}")
            print(f"{fav_movie} : {type(fav_movie)}")
            try:
                ratio = fuzz.ratio(title.lower(), fav_movie.lower())
                if ratio >= 60:
                    match_tuple.append((title, idx, ratio))
            except AttributeError:
                pass

        # sort
        match_tuple = sorted(match_tuple, key=lambda x: x[2])[::-1]
        if not match_tuple:
            print('Oops! No match is found')
        else:
            print('Found possible matches in our database: '
                  '{0}\n'.format([x[0] for x in match_tuple]))
            return match_tuple[0][1]

    def _inference(self, model, data, hashmap,
                   fav_movie, n_recommendations):
        """
        return top n similar movie recommendations based on user's input movie
        Parameters
        ----------
        model: sklearn model, knn model
        data: movie-user matrix
        hashmap: dict, map movie title name to index of the movie in data
        fav_movie: str, name of user input movie
        n_recommendations: int, top n recommendations
        Return
        ------
        list of top n similar movie recommendations
        """
        # fit
        model.fit(data)
        # get input movie index
        print('You have input movie:', fav_movie)
        idx = self._idx_lookup(hashmap, fav_movie)
        # inference
        print('Recommendation system start to make inference')
        print('......\n')
        t0 = time.time()
        distances, indices = model.kneighbors(
            data[idx],
            n_neighbors=n_recommendations + 1)
        # get list of raw idx of recommendations
        raw_recommends = \
            sorted(
                list(
                    zip(
                        indices.squeeze().tolist(),
                        distances.squeeze().tolist()
                    )
                ),
                key=lambda x: x[1]
            )[:0:-1]
        print('It took my system {:.2f}s to make inference \n\
              '.format(time.time() - t0))
        # return recommendation (movieId, distance)
        return raw_recommends

    def make_recommendations(self, n_recommendations):
        """
        make top n movie recommendations
        Parameters
        ----------
        fav_movie: str, name of user input movie
        n_recommendations: int, top n recommendations
        """
        # get data
        movie_user_mat_sparse, hashmap = self._prep_data()

        # get recommendations
        for fav_movie in self.movie_set:
            raw_recommends = self._inference(
                self.model, movie_user_mat_sparse, hashmap,
                fav_movie, n_recommendations)

            raw_recommends = sorted(raw_recommends, key=lambda x: x[1])

            # print and package results
            recommendations = []
            reverse_hashmap = {v: k for k, v in hashmap.items()}

            print('Recommendations for {}:'.format(fav_movie))
            for i, (idx, dist) in enumerate(raw_recommends):
                try:
                    print('{0}: {1}, with distance '
                          'of {2}'.format(i + 1, reverse_hashmap[idx], dist))
                    recommendations.append((reverse_hashmap[idx], dist))
                except KeyError:
                    print('{0}: {1}, with distance '
                          'of {2}'.format(i + 1, "RANDOM", 99))
                    recommendations.append((self.final_movie_df.sample(1)['title'].values[0], dist))

            self.recommendations[fav_movie] = recommendations

    def return_recommendations(self):

        '''
        returns 5 recommendations based on user input exploration level
        :return: data frame of movie title and distance
        '''

        title_list = []
        for movie in self.movie_set:
            title = self.recommendations[movie][self.exploration][0]
            title_list.append(title)

        data = self.final_movie_df[self.final_movie_df['title'].isin(title_list)]\
                    .sort_values("year", ascending=False)\
                    .reset_index()

        return data
