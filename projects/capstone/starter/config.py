import os

basedir = os.path.abspath(os.path.dirname(__file__))


class DBConfig:
    DEBUG = True
    SECRET_KEY = os.urandom(32)  # TODO: Change secret
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

bearer_tokens = {
"casting_assistant": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InBlRmF2ZGM3TjE1RldRaE82ZXNHSiJ9.eyJpc3MiOiJodHRwczovL3RheWxvcmZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY0ZDQ0MGUxNzIwN2UwMWYyZDk0YjhjNCIsImF1ZCI6IkNhc3RpbmciLCJpYXQiOjE2OTk3NTAxOTQsImV4cCI6MTY5OTc1NzM5NCwiYXpwIjoiT1hKbXFMQU5yd1ducWdoTnp3eFdHWmdsUVZUUDN5UnYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.eivu1Vo9ipCJfx7g_v4O4oKM_iucpqBH6CuX0XEwb_QqAEEiyYPPx9N7cFaZ4bAo-PTpJfFmq6Eraugsei_qYOYYTj9SpFMyuns-8_etoxZ8Yob_fWDasjrFrgYqpBYdjlrzVClECQYyDpCMrl6bVeE6vAsyXg1E35L7G5o8fS_PmoTqVOwenQnlr-VeZdLz1feSSwN13vdES5RKy23ukTCnVLhDhuDob6uSx7cBiciCDv7717ORTa48GzTpT4BXiOVpjl9Iu9zdLSUV28Z-ZPlaDxpYVpCpaVHjMuognPYgnT0WTYGlWCAUCpGHC8gJMrL-6Ii8BKltm2Cm1yWHqA"
}

class Auth0Config:
    domain = 'taylorfsnd.us.auth0.com'
    algorithms = ['RS256']
    audience = 'Casting'