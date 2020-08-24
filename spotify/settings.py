
import os
import sys

basedir=os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig():
    SECRET_KEY='lrabbit'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PER_PAGE=12

    #whooshee
    WHOOSHEE_MIN_STRING_LEN=1



class DevelopmentConfig(BaseConfig):

    SQLALCHEMY_DATABASE_URI = \
        prefix + os.path.join(basedir, 'data-dev.db')
    REDIS_URL = "redis://localhost"

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        prefix + os.path.join(basedir, 'data.db'))
    pass


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'  # in-memory database
    WTF_CSRF_ENABLED = False


config={
    'testing': TestingConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig

}








