from twitterauth.configs.base import Settings
settings = Settings()

if not settings.configured:
    settings.configure()
