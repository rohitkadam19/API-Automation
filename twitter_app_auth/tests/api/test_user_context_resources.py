import json
import logging

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings
from twitterauth.utils import helper
from twitterauth.utils import payload

LOGGER = logging.getLogger('twitter')
restricted_resource_user_err_msg = 'Your credentials do not allow access to this resource'


class TestUserContextAPI(APITestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_unathorized_user_context_resource_using_appauth(self):
        """
        Verify app only authentication gets error when try to access resources
        which needs user session.
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

        # Verify /statuses/mentions_timeline using access_token retrieved from above step
        oheaders = {'Authorization': 'Bearer ' + parsed_response['access_token'],
                    'Accept-Encoding': 'application/gzip'}
        user_tline_resp = self.session.get(self.base_url + '/1.1/statuses/mentions_timeline',
                                           headers=oheaders)
        assert user_tline_resp.status_code == 403
        LOGGER.info(user_tline_resp.text)

        # Verify error message in response
        assert user_tline_resp.text.strip("\n") == restricted_resource_user_err_msg
