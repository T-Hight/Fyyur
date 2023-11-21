# Casting Agency Capstone Project

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

#### Python

Before getting started, you'll need to download Python. Instructions for downloading this version can be found here: [Python 3.7](https://www.python.org/downloads/release/python-370/)

#### Virtual Environment

Next, you'll want to run a virtual environment on your local machine to keep your dependencies seperate and organized. Instructions to create and run a virtual environment can be found here: [python docs](https://docs.python.org/3/library/venv.html) 

#### Dependencies

After you have your virtual environment created and running, it's time to install the required dependencies for the project with:

```bash
pip install -r requirements.txt
```
This will install all of the required packages within the **requirements.txt** file.

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [PostgreSQL](https://www.postgresql.org/) and [psycopg2](https://pypi.org/project/psycopg2/) to handle data persistence and database management.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

- [jose](https://python-jose.readthedocs.io/en/latest/) is JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

- [Auth0](https://auth0.com/) to manage authentication and permissions.

### Set up the Database

With Postgres running, create a `Casting` database:

```bash
createdb Casting
```

Populate the database using the `Casting.psql` file provided. From the `capstone` folder in terminal run:

```bash
psql Casting < Casting.psql
```

### Run the Server

From within the `capstone` folder, first ensure you are working using your created virtual environment.

To run the server using your GIT Bash Terminal, execute:

```bash
bash setup.sh
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --debug
```

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application called 'Casting'
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:actors`
   - `get:movies`
   - `post:actors`
   - `post:movies`
   - `patch:actors`
   - `patch:movies`
   - `delete:actors`
   - `delete:movies`
6. Create new roles for:
   - Casting Assistant
     - can `get:actors`
     - can `get:movies`
   - Casting Director
     - can `get:actors`
     - can `get:movies`
     - can `post:actors`
     - can `patch:actors`
     - can `patch:movies`
     - can `delete:actors`
   - Executive Producer
     - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com).
   





