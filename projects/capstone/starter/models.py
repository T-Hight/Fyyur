import os
from flask_sqlalchemy import SQLAlchemy
import json
from flask_migrate import Migrate
from sqlalchemy import ForeignKey, Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from config import DBConfig, Auth0Config

db_user = os.getenv('db_user', 'postgres')
db_password = os.getenv('db_password', 'postgres')
db_host = os.getenv('db_host', 'localhost:5432')
db_name = os.getenv('db_name','Casting')
db_path = 'postgresql://{}:{}@{}/{}'.format(
    db_user, db_password, db_host, db_name
)

db = SQLAlchemy()

def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    #migrate = Migrate(app, db)
    with app.app_context():
        db.create_all()

class Movies(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer(), primary_key=True)
    title = Column(String(120))
    release_date = Column(DateTime)
    actors = relationship('Actors', backref="movie", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'actors': [actor.format() for actor in self.actors]
        }

    def __repr__(self):
       return '<Movies {}'.format(self.title)
    
class Actors(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    age = Column(String(120))
    gender = Column(String(120))
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=True)

    def __init__(self, name, age, gender, movie_id):
        self.name = name
        self.age = age
        self.gender = gender
        self.movie_id = movie_id

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            "movie_id": self.movie_id
        }

    def __repr__(self):
       return '<Actors {}'.format(self.name)