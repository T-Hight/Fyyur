import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movies, Actors
from datetime import datetime
from auth import AuthError, requires_auth

def create_app(db_URI="", test_config=None):
 
  app = Flask(__name__)
  
  CORS(app, resources={"/": {"origins": "*"}})
  
  if db_URI:
    setup_db(app, db_URI)
  else:
     setup_db(app)

  @app.after_request
  def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,PATCH,DELETE,OPTIONS')
    return response


  @app.route('/')
  def hello():
    return 'Hello, World!'
  
  # GET /actors
  # This endpoint should be accessable by all parties
  # and return a list of actors in json form.

  @app.route('/actors')
  
  @requires_auth('get:actors')
  
  def get_actors(payload):
      try:
          actors = Actors.query.all()
          return jsonify(
            {
                "success": True,
                "actors": [actor.format() for actor in actors]
            }
          ), 200
      
      except Exception as e:
          print('debug')
          print(e)
          abort(422)

  # GET /actors/<int:id>
  # This endpoint should be accessable by all parties
  # and return a specified actor in json form.

  @app.route('/actors/<int:id>')

  @requires_auth('get:actors')

  def get_actor(payload, id):
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

  # GET /movies
  # This endpoint should be accessable by all parties
  # and return a list of movies.

  @app.route('/movies')

  @requires_auth('get:movies')

  def get_movies(payload):
      try:
        movies = Movies.query.all()
        return jsonify(
            {
              "success": True,
              "movies": [movie.format() for movie in movies]
            }
        ), 200
      
      except Exception as e:
        print('debug')
        print(e)
        abort(422)

  # GET /movies/<int:id>
  # This endpoint should be accessable by all parties
  # and return a specified movie in json form. 

  @app.route('/movies/<int:id>')
  
  @requires_auth('get:movies')

  def get_movie(payload, id):
    movie = Movies.query.get(id)
    if movie:
      return jsonify(
      {
          "success": True,
          "movie": [movie.format()]
      }
    ), 200
    
    else:
        print("movie id not found")
        abort(404) 

  # POST /actors
  # This endpoint should be accessable by Casting Directors 
  # and Executive Producers only

  @app.route('/actors', methods=['POST'])

  @requires_auth('post:actors')

  def post_actors(payload):
    body = request.get_json()

    name = body.get('name')
    age = body.get('age')
    gender = body.get('gender')

    if len(name) == 0 or len(age) == 0 or len(gender) == 0:
        abort(404)

    try:
        actor = Actors(
          name=name,
          age=age,
          gender=gender
        )

        actor.insert()

        return jsonify(
          {
              'success': True,
              'actor': [actor.format()]
          }
        ), 200
    
    except Exception as e:
      print('debug')
      print(e)
      abort(422)

  # POST /movies
  # This endpoint should be accessable by Executive Producers only

  @app.route('/movies', methods=['POST'])

  @requires_auth('post:movies')

  def post_movie(payload):
    body = request.get_json()

    title = body.get('title')
    release_date = body.get('release_date')

    if len(title) == 0:
      abort(404)

    try:
      movie = Movies(
        title=title,
        release_date=release_date
      )

      movie.insert()

      return (
        {
            "success": True,
            "movie": [movie.format()]
        }
      ), 200

    except Exception as e:
      print('debug')
      print(e)
      abort(422)

  # PATCH /actors
  # This endpoint should be accessable by Casting Directors 
  # and Executive Producers only

  @app.route('/actors/<int:id>', methods = ['PATCH'])

  @requires_auth('patch:actors')

  def patch_actors(payload, id):
    actor = Actors.query.get(id)

    body = request.get_json()

    if not actor:
        abort(404)

    try:
      name = body.get('name')
      age = body.get('age')
      gender = body.get('gender')

      if name:
        actor.name = name

      if age:
        actor.age = age

      if gender:
        actor.gender = gender

      actor.update()

      return jsonify(
        {
          "success": True,
          "actor": actor
        }
      ), 200
    
    except Exception as e:
      print('debug')
      print(e)
      abort(422)

  # PATCH /movies
  # This endpoint should be accessable by Casting Directors 
  # and Executive Producers only

  @app.route('/movies/<int:id>', methods = ['PATCH'])

  @requires_auth('patch:movies')

  def patch_movies(payload, id):
    movie = Actors.query.get(id)

    body = request.get_json()

    if not movie:
        abort(404)

    try:
      title = body.get('title')
      release_date = body.get('release_date')

      if title:
        movie.title = title

      if release_date:
        movie.release_date = release_date

      movie.update()

      return jsonify(
        {
          "success": True,
          "movie": movie
        }
      ), 200
    
    except Exception as e:
      print('debug')
      print(e)
      abort(422)

  # DELETE /actors/<int:id>
  # This endpoint should be accessable by Casting Directors 
  # and Executive Producers only

  @app.route('/actors/<int:id>', methods = ['DELETE'])

  @requires_auth('delete:actors')

  def delete_actor(payload, id):
    try:
      actor = Actors.query.get(id)

      if actor:
          actor.delete()

          return jsonify(
            {
                "success": True,
                "delete": id
            }
          ), 200
      else:
          abort(404)
   
    except Exception as e:
      print('debug')
      print(e)
      abort(422)
  
  # DELETE /movies/<int:id>
  # This endpoint should be accessable by Casting Directors 
  # and Executive Producers only

  @app.route('/movies/<int:id>', methods = ['DELETE'])

  @requires_auth('delete:movies')

  def delete_movie(payload,id):
    try:
      movie = Movies.query.get(id)

      if movie:
          movie.delete()

          return jsonify(
            {
                "success": True,
                "delete": id
            }
          ), 200
      else:
          abort(404)
   
    except Exception as e:
      print('debug')
      print(e)
      abort(422)

  #ErrorHandlers

  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          "success": False,
          "error": 422,
          "message": "Unprocessable"
      }), 422
  
  @app.errorhandler(404)
  def resource_not_found(error):
      return jsonify({
          "success": False,
          "error": 404,
          "message": "Resource Not Found"
      }), 404
  
  @app.errorhandler(AuthError)
  def unauthorized(error):
    return jsonify({
       "success": False,
       "error": 401,
       "message": "Unauthorized"
    }), 401
      


  return app

APP = create_app()

if __name__ == '__main__':
  APP.run(host='0.0.0.0', port=8080, debug=True)