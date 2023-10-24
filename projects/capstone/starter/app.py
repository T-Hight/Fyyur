import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from datetime import datetime


#from auth.auth import AuthError, requires_auth



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.after_request
    def after_request(response):
      response.headers.add(
          'Access-Control-Allow-Headers',
          'Content-Type,Authorization,true')
      response.headers.add(
          'Access-Control-Allow-Methods',
          'GET,PUT,POST,DELETE,OPTIONS')
      return response


    @app.route('/')
    def hello():
      return 'Hello, World!'

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=8080, debug=True)