import os

from app import app


def get_image_filename(id):
    """
    Gets the filename of a video game artwork by its ID
    :param id: the video game identifier
    :return: the filename of the image
    """
    for filename in os.listdir(app.config['UPLOAD_PATH']):
        if 'artwork_{}'.format(id) in filename:
            return filename
    return 'default.jpg'


def delete_image(id):
    """
    Removes a image file from the uploads directory
    :param id: the video game identifier for which the file will be removed
    """
    image_filename = get_image_filename(id)
    if image_filename != 'default.jpg':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], image_filename))
