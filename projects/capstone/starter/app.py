import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movies, Actors, db

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app, resources={"/": {"origins": "*"}})

  #if db_URI:
      #setup_db(app,db_URI)
  #else:
      #setup_db(app)

  @app.route('/')
  def hello():
    return 'Hello, World!'

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=8080, debug=True)