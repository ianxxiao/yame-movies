from google_images_search import GoogleImagesSearch

def get_moive_image(movie_name):

    """
    This function look up a image based on the movie name.
    movie_name (str): the name of the movie
    :return:
    img_url (str): a url to the photo file of the movie
    """

    gis = GoogleImagesSearch('your_dev_api_key', 'your_project_cx')
    _search_params = {}
    img_url = None

    return img_url