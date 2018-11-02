import requests
from twitterauth.configs import Settings


def singleton(self):
    """
    Returns same instance if already created
    :param self:
    :return:
    """
    instances = {}

    def get_instance():
        if self not in instances:
            instances[self] = self()
        return instances[self]
    return get_instance


@singleton
class Session:
    """
    Requests session object
    """
    def __init__(self):
        self.session = None
        self.settings = Settings()

    def get_session(self):
        """
        Returns requests sesssion object
        Returns if already created or creates new one
        :return:
        """
        if self.session is None:
            return self._create_session()
        else:
            return self.session

    def _create_session(self):
        """
        Function to set all values required for session
        :return:
        """
        self.session = requests.Session()
        self.session.verify = None

        return self.session
