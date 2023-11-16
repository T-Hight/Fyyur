import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors



class CastingTestCase(unittest.TestCase):


    def setUp(self):
        """Define test variables and initialize app."""
        self.database_name = "Casting"
        self.database_path = self.database_path = "postgresql://{}:{}@{}/{}".format('postgres','postgres','localhost:5432',self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        #setup_db(self.app, self.database_path)

        # binds the app to the current context
        #with self.app.app_context():
           # self.db = SQLAlchemy()
           # self.db.init_app(self.app)
           # self.db.create_all()
        self.assistant_header = os.environ.get('ASSISTANT_TOKEN')
        self.director_header = os.environ.get('DIRECTOR_TOKEN')
        self.producer_header = os.environ.get('PRODUCER_TOKEN')
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_hello_world(self):
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])

    def test_get_actors_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], 'Authorization header missing') 

    def test_get_actor(self):
        res = self.client().get('/actors/1', headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["actors"])

    def test_get_actor_401(self):
        res = self.client().get('/actors/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], 'Authorization header missing') 
    
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])

    def test_get_movies_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], 'Authorization header missing') 

    def test_get_movie(self):
        res = self.client().get('/movies/1', headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertTrue(data["movies"])

    def test_get_movies_401(self):
        res = self.client().get('/movies/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], 'Authorization header missing') 

    def test_post_movie_401(self):
        self.new_movie = {
            "title": "The Santa Clause",
            "release_date": "2004-01-21 00:00:00"
        }
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], "Unauthorized")
    
    def test_post_movie(self):
        self.new_movie = {
            "title": "The Santa Clause",
            "release_date": "2004-01-21 00:00:00"
        }
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
    
    def test_post_actor_401(self):
        self.new_actor = {
            "name": "Toby McGuire",
            "age": "33",
            "gender": "male",
            "movie_id": 4
        }
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], "Unauthorized")
    
    def test_post_actor(self):
        self.new_actor = {
            "name": "Toby McGuire",
            "age": "33",
            "gender": "male",
            "movie_id": 4
        }
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_edit_actor(self):
        edit_actor_age = {
            "age": "24"
        }
        res = self.client().patch('/actors/2', json=edit_actor_age, headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_edit_actor_404(self):
        edit_actor_age = {
            "age": "24"
        }
        res = self.client().patch('/actors/22', json=edit_actor_age, headers={'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], "Resource Not Found")

    def test_edit_movie(self):
        edit_movie_title = {
            "title": "Jaws 2"
        }
        res = self.client().patch('/movies/1', json=edit_movie_title, headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def test_edit_movie_404(self):
        edit_movie_title = {
            "title": "Jaws 2"
        }
        res = self.client().patch('/movies/11', json=edit_movie_title, headers={'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertTrue(data["success"])
        self.assertTrue(data["message"], "Resource Not Found")

    def delete_actor(self):
        res = self.client().delete('/actors/3', headers = {'Authorization': self.director_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def delete_actor_401(self):
        res = self.client().delete('/actors/1', headers = {'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], "Unauthorized")

    def delete_movie(self):
        res = self.client().delete('/movies/3', headers = {'Authorization': self.producer_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])

    def delete_movie_401(self):
        res = self.client().delete('/movies/1', headers = {'Authorization': self.assistant_header})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertTrue(data["message"], "Unauthorized")


if __name__ == "__main__":
    unittest.main()

