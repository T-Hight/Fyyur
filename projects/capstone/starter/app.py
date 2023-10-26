import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from datetime import datetime
#from .auth.auth import AuthError, requires_auth



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
    
    @app.route('/actors')
    
    #@requires_auth('get:actors')
    
    def get_actors():
        try:
            actors = [actor.format() for actor in Actors.query.all()]
            return jsonify(
              {
                  "success": True,
                  "actors": actors
              }
            ), 200
        
        except Exception as e:
           print('debug')
           print(e)
           abort(422)

    @app.route('/actors/<int:id>')

    #@requires_auth('get:actors')

    def get_actor(id):
      actor = Actors.query.get(id)
      if actor:
        return jsonify(
        {
            "success": True,
            "actor": [actor.format()]
        }
      ), 200
      
      else:
         print("actor id not found")
         abort(404)
       
       

    @app.route('/movies')

    #@requires_auth('get:movies')

    def get_movies():
       try:
          movies = Movies.query.all()
          movies = list(map(lambda movie: movie.format(), movies))
          return jsonify(
             {
                "success": True,
                "movies": movies
             }
          )
       
       except Exception as e:
          print('debug')
          print(e)
          abort(422)

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='localhost', port=8080, debug=True)