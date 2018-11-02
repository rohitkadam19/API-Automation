import json
import logging

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings
from twitterauth.utils import helper
from twitterauth.utils import payload

LOGGER = logging.getLogger("twitter")
invalid_creds_err_msg = "Unable to verify your credentials"


class TestInvalidUserCredentials(APITestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_oauth_with_invalid_creds(self):
        """
          Verify twitter auth API returns error when passed
          invalid credentials.
        """
        headers = payload.get_oauth_headers("invalid_creds")
        data = payload.get_oauth_data()

        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 403
        LOGGER.info(response.text)

        # Assert error message for invalid credentials
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_creds_err_msg

    def test_oauth_with_invalid_consumer_key(self):
        """
          Verify twitter auth API returns error when passed
          invalid consumer key.
        """
        headers = payload.get_oauth_headers(
            helper.getBase64Value(
                consumer_key="invalid_consumer_key"
            ))
        data = payload.get_oauth_data()

        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 403
        LOGGER.info(response.text)

        # Assert error message for invalid credentials
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_creds_err_msg

    def test_oauth_with_invalid_secret_key(self):
        """
          Verify twitter auth API returns error when passed
          invalid secret key.
        """
        headers = payload.get_oauth_headers(
            helper.getBase64Value(
                secret_key="invalid_secret_key"
            ))
        data = payload.get_oauth_data()

        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 403
        LOGGER.info(response.text)

        # Assert error message for invalid credentials
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_creds_err_msg

    def test_oauth_with_other_acc_consumer_key(self):
        """
          Verify twitter auth API returns error when passed
          consumer key of one account and  secret key of other account.
        """
        headers = payload.get_oauth_headers(
            helper.getBase64Value(
                consumer_key=settings.api.other_acc_consumer_key
            ))
        data = payload.get_oauth_data()

        response = self.session.post(self.base_url + "/oauth2/token",
                                     data=data,
                                     headers=headers)
        assert response.status_code == 403
        LOGGER.info(response.text)

        # Assert error message for invalid credentials
        parsed_response = json.loads(response.text)
        assert parsed_response["errors"][0]["message"] == \
               invalid_creds_err_msg
