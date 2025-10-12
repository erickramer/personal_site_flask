import os


class Config:
    """Base config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-please-change')
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development config."""
    DEBUG = True


class TestingConfig(Config):
    """Testing config."""
    TESTING = True


class ProductionConfig(Config):
    """Production config."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'production-key-required')

    # Production-specific security settings
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
