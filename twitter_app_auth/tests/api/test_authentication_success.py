import json
import logging

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings
from twitterauth.utils import helper
from twitterauth.utils import payload

LOGGER = logging.getLogger('twitter')


class TestAuthenticationSuccess(APITestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_authentication_successful(self):
        """
        Verify successful authentication message with
        valid access token
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())
        data = payload.get_oauth_data()

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + '/oauth2/token',
                                     data=data,
                                     headers=headers)
        assert response.status_code == 200
        LOGGER.info(response.text)
        parsed_response = json.loads(response.text)

        # Verify /statuses/user_timeline using access_token retrieved from above step
        oheaders = {'Authorization': 'Bearer ' + parsed_response['access_token'],
                    'Accept-Encoding': 'application/gzip'}
        user_tline_resp = self.session.get(self.base_url +
                                           '/1.1/statuses/user_timeline.json?count=100&screen_name=twitterapi',
                                           headers=oheaders)
        assert user_tline_resp.status_code == 200

