import json
import logging

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings

LOGGER = logging.getLogger('twitter')
invalid_bearer_token_err_msg = 'Invalid or expired token.'


class TestInvalidBearerToken(APITestCase):

    @classmethod
    def setUpClass(self):
        print "In setup class"
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_get_user_timeline_with_invalid_bearer_token(self):
        """
        Verify error message when passed invalid bearer token
        """

        oheaders = {"Authorization": "Bearer " + "Invalid bearer token",
                   "Accept-Encoding": "application/gzip"}
        user_tline_resp = self.session.get(self.base_url +
                                           "/1.1/statuses/user_timeline.json?count=100&screen_name=twitterapi",
                                           headers=oheaders)
        LOGGER.info(user_tline_resp.text)
        parsed_response = json.loads(user_tline_resp.text)
        # Verify error message in response
        assert parsed_response["errors"][0]["message"] == \
               invalid_bearer_token_err_msg
