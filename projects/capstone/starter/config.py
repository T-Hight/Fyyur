import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DBConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(32)  # TODO: Change secret
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')


class Auth0Config:
    domain = os.getenv('AUTH0_DOMAIN')
    algorithms = [os.getenv('AUTH0_ALGORITHMS')]
    audience = os.getenv('AUTH0_AUDIENCE')