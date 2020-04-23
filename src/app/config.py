import os
basedir = os.path.abspath(os.path.dirname(__file__))
DBUSER = os.environ.get("POSTGRES_USER", "tellor")
DBPASS = os.environ.get("POSTGRES_PASSWORD", "tellor")
DBHOST = os.environ.get("POSTGRES_HOST", "postgres")
DBPORT = os.environ.get("POSTGRES_PORT", 5432)
DBNAME = os.environ.get("POSTGRES_DB", "tellor")
BACKEND_USERNAME = os.environ.get("BACKEND_USERNAME", "tellor")
BACKEND_PASSWORD = os.environ.get("BACKEND_PASSWORD", "tellor")


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    BACKEND_PASSWORD = BACKEND_PASSWORD
    BACKEND_USERNAME = BACKEND_USERNAME
    SECRET_KEY = 'saltandpepper'
    SQLALCHEMY_DATABASE_URI = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
