import json
import logging
import time

from twitterauth.session import Session
from twitterauth.test import APITestCase
from twitterauth.configs import settings
from twitterauth.utils import helper
from twitterauth.utils import payload

LOGGER = logging.getLogger('twitter')
USER_TIMELINE_LIMIT = 1500


class TestTwitterAuthRateLimiting(APITestCase):

    @classmethod
    def setUpClass(self):
        self.session = Session().get_session()
        self.base_url = settings.api.url

    def test_statuses_utline_rate_limit(self):
        """
        Verify limit change in user timeline statuses
        after executing it 3 times.
        """
        headers = payload.get_oauth_headers(helper.getBase64Value())
        data = payload.get_oauth_data()

        # Get bearer token using /oauth2/token
        response = self.session.post(self.base_url + '/oauth2/token',
                                     data=data,
                                     headers=headers)
        assert response.status_code == 200
        parsed_response = json.loads(response.text)

        # Hit /statuses/user_timeline 3 times to check if count changes
        oheaders = {'Authorization': 'Bearer ' + parsed_response['access_token'],
                    'Accept-Encoding': 'application/gzip'}

        for x in range(0, 3):
            self.session.get(self.base_url + '/1.1/statuses/user_timeline.json?count=100&screen_name=twitterapi',
                             headers=oheaders)

        time.sleep(5)

        # Get rate limit status for statuses resource
        user_rlimit_resp = self.session.get(self.base_url +
                                            '/1.1/application/rate_limit_status.json?resources=statuses',
                                            headers=oheaders)

        assert user_rlimit_resp.status_code == 200

        parsed_rlimit_resp = json.loads(user_rlimit_resp.text)
        assert parsed_rlimit_resp['resources']['statuses']['/statuses/user_timeline']['remaining'] \
               < USER_TIMELINE_LIMIT
