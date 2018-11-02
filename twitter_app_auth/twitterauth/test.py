import logging
import unittest2
from twitterauth.configs import settings


LOGGER = logging.getLogger(__name__)


class TestCase(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestCase, cls).setUpClass()
        if not settings.configured:
            settings.configure()

    @classmethod
    def tearDownClass(cls):
        logging.info("In teardown class")

    def setUp(self):
        LOGGER.info("Started test : ")

    def tearDown(self):
        LOGGER.info("Finished test : ")


class APITestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super(APITestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(APITestCase, cls).tearDownClass()
