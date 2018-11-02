import base64
import os

from twitterauth.configs import settings


def get_project_root():
    """
    Return the path to the twitter_app_auth project root directory.
    :return: A directory path.
    :rtype: str
    """
    return os.path.realpath(os.path.join(
         os.path.dirname(__file__),
         os.pardir,
         os.pardir,
    ))


def getBase64Value(consumer_key=settings.api.consumer_key,
                   secret_key=settings.api.consumer_secret):
    """
    Return base64 encoded string
    :param consumer_key:
    :param secret_key:
    :return:
    """
    return base64.b64encode(consumer_key + ":" + secret_key)

