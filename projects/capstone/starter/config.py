import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DBConfig:
    DEBUG = True
    SECRET_KEY = os.getenv('AUTH0_SECRET')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ('postgres://casting_gr1i_user:5ba9UGeWI7W3xJ8nvsY2k0k0yptZZiDa@dpg-clf51pkp3ifc7390l630-a/casting_gr1i')

class Auth0Config:
    domain = os.getenv('AUTH0_DOMAIN')
    algorithms = [os.getenv('AUTH0_ALGORITHMS')]
    audience = os.getenv('AUTH0_AUDIENCE')