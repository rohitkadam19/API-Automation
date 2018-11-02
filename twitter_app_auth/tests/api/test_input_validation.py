import json
import logging

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings
from twitterauth.utils import helper
from twitterauth.utils import payload

LOGGER = logging.getLogger('twitter')
grant_type_missing_err_msg = 'Missing required parameter: grant_type'
invalid_creds_err_msg = 'Unable to verify your credentials'
invalid_grant_type_err_msg = 'invalid_grant_type_value parameter is invalid'


class TestTwitterAuthAPIInputValidation(APITestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_oauth_without_grant_type(self):
        """
        Verify twitter oauth without grant_type
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + "/oauth2/token",
                                     headers=headers)

        # Verify error status code and error message
        assert response.status_code == 403
        LOGGER.info(response.status_code)
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               grant_type_missing_err_msg

    def test_oauth_with_invalid_grant_type(self):
        """
        Verify twitter oauth with invalid grant_type
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())
        data = payload.get_oauth_data(grant_type="invalid_grant_type_value")

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)

        # Verify error status code and error message
        assert response.status_code == 400
        LOGGER.info(response.status_code)
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_grant_type_err_msg

    def test_oauth_without_content_type(self):
        """
        Verify twitter oauth without content_type
        """
        headers = payload.get_oauth_headers(helper.getBase64Value(),
                                            content_type="")

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + "/oauth2/token",
                                     headers=headers)

        # Verify error status code
        assert response.status_code == 403
        LOGGER.info(response.status_code)

    def test_oauth_without_authorization(self):
        """
        Verify twitter oauth without authorization
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())
        data = payload.get_oauth_data()

        headers.pop('Authorization', None)

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 403
        LOGGER.info(response.text)

        # Verify error message in response
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_creds_err_msg

    def test_oauth_invalid_url(self):
        """
        Verify twitter oauth with invalid oauth url
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())
        data = payload.get_oauth_data()

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + "/oauth2",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 404
