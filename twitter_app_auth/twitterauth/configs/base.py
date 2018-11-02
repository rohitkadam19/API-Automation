import os
import sys
import logging
import configparser
from logging import config

LOGGER = logging.getLogger(__name__)
SETTINGS_FILE_NAME = 'twitter_auth.conf'


def get_project_root():
    """Return the path to the Twitter auth project root directory.
    :return: A directory path.
    :rtype: str
    """
    return os.path.realpath(os.path.join(
         os.path.dirname(__file__),
         os.pardir,
         os.pardir,
    ))


class PropertyReader(object):

    def __init__(self, Path):
        self.config_parser = configparser.ConfigParser()
        with open(Path) as handler:
            self.config_parser.readfp(handler)
            if sys.version_info[0] < 3:
                # ConfigParser.readfp is deprecated on Python3, read_file
                # replaces it
                self.config_parser.readfp(handler)
            else:
                self.config_parser.read_file(handler)

    def get(self, section, option, default=None):
        try:
            value = self.config_parser.get(section, option)
        except Exception as e:
            value = default
        return value

    def has_section(self, section):
        """Check if section is present"""
        return self.config_parser.has_section(section)


class ImproperlyConfigured(Exception):
    """Twitter app auth is improperly configured
    If settings file is not present, it will
    raise this exception
    """


class FeatureSettings(object):
    """
    Create a instance of this class and assign attributes to map to the feature
    options.
    """
    def read(self, reader):
        """
        Subclasses must implement this method in order to populate itself
        with expected settings values.
        :param reader:
        :return:
        """

        raise NotImplementedError('Subclasses must implement read method.')

    def validate(self):
        """Subclasses must implement this method in order to validade the
        settings and raise ``ImproperlyConfigured`` if any issue is found.
        """

        raise NotImplementedError('Subclasses must implement read method.')


class TwitterAuthAPISettings(FeatureSettings):
    def __init__(self,*args, **kwargs):
        super(TwitterAuthAPISettings, self).__init__(*args, **kwargs)
        self.url = None
        self.consumer_key = None
        self.consumer_secret = None
        self.other_acc_consumer_key = None

    def read(self, reader):
        self.url = reader.get(
            'twitter_api', 'url',
            "https://api.twitter.com"
        )
        self.consumer_secret = reader.get(
            'twitter_api', 'consumer_secret'
        )
        self.consumer_key = reader.get(
            'twitter_api', 'consumer_key'
        )
        self.other_acc_consumer_key = reader.get(
            'twitter_api', 'other_acc_consumer_key'
        )

    def validate(self):
        validation_errors = []
        if None in [self.consumer_secret, self.consumer_key]:
            validation_errors.append(
                'Consumer key or secret is not provided'
            )
        elif self.consumer_key == "" or self.consumer_secret == "":
            validation_errors.append(
                'Consumer key or secret is empty'
            )
        return validation_errors


class Settings(object):

    def __init__(self):
        self._all_features = None
        self._configured = False
        self.reader = None
        self._validation_errors = []

        self._configure_logging()
        self.api = TwitterAuthAPISettings()

    def configure(self):
        if self.configured:
            return

        settings_path = os.path.join(get_project_root(), SETTINGS_FILE_NAME)
        if not os.path.isfile(settings_path):
            raise ImproperlyConfigured(
                'Not able to find settings file at {}'.format(settings_path))

        self.reader = PropertyReader(settings_path)

        if self.reader.has_section('twitter_api'):
            self.api.read(self.reader)
            self._validation_errors.extend(self.api.validate())

        print(self._validation_errors)
        if self._validation_errors:
            raise ImproperlyConfigured(
                'Failed to validate the configuration, check the message(s):\n'
                '{}'.format('\n'.join(self._validation_errors))
            )

        self._configured = True

    def _configure_logging(self):
        """Configure logging for Twitter Auth App.

        It will load configuration from logging.conf if present
        in root directory, otherwise custom logging format is used by
        default

        """

        if self.configured:
            LOGGER.info("Already configured")
            return

        # All output should be made by the logging module, including warnings
        logging.captureWarnings(True)

        # Allow overriding logging config based on the presence of logging.conf
        # file on Twitter Auth app's project root
        logging_conf_path = os.path.join(get_project_root(), 'logging.conf')
        if os.path.isfile(logging_conf_path):
            config.fileConfig(logging_conf_path)
        else:
            logging.basicConfig(
                format='%(levelname)s %(module)s:%(lineno)d: %(message)s'
            )

    @property
    def configured(self):
        """Returns True if the settings have already been configured."""
        return self._configured

    @property
    def all_features(self):
        """List all expected feature settings sections."""
        if self._all_features is None:
            self._all_features = [
                name for name, value in vars(self).items()
                if isinstance(value, FeatureSettings)
            ]
        return self._all_features
