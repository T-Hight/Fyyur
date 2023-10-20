import os
from flask_sqlalchemy import SQLAlchemy

db_user = os.getenv('db_user', 'postgres')
db_password = os.getenv('db_password', 'postgres')
db_host = os.getenv('db_host', 'localhost:5432')
db_name = os.getenv('db_name','Casting')
db_path = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    db_user, db_password, db_host, db_name
)

db = SQLAlchemy()

def setup_db(app, database_path=db_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.create_all()

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    release_date = db.Column(db.String(120))

    def __repr__(self):
       return '<Movies {}'.format(self.name)
    
class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))

    def __repr__(self):
       return '<Actors {}'.format(self.name)