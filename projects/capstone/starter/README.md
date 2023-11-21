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
   
## API Endpoint Behavior

#### GET /actors

This endpoint should be accessable by all parties and return a list of actors in json form.

```json
{
  "actors": [
    {
      "age": "43",
      "gender": "male",
      "id": 1,
      "movie_id": 3,
      "name": "Ray Charles"
    },
    {
      "age": "23",
      "gender": "male",
      "id": 2,
      "movie_id": 1,
      "name": "Gus Demeter"
    },
    {
      "age": "31",
      "gender": "female",
      "id": 3,
      "movie_id": 2,
      "name": "Sarah Chase"
    }
  ],
  "success": true
}
```

#### GET /actors/<int:id>

This endpoint should be accessable by all parties and return a specified actor in json form.

```json
{
  "actors": [
    {
      "age": "43",
      "gender": "male",
      "id": 1,
      "movie_id": 3,
      "name": "Ray Charles"
    }
  ],
  "success": true
}
```  

#### GET /movies

This endpoint should be accessable by all parties
and return a list of movies in json form.

```json
{
  "movies": [
    {
      "actors": [
        {
          "age": "23",
          "gender": "male",
          "id": 2,
          "movie_id": 1,
          "name": "Gus Demeter"
        }
      ],
      "id": 1,
      "release_date": "Tue, 06 Dec 1983 00:00:00 GMT",
      "title": "Jaws"
    },
    {
      "actors": [
        {
          "age": "31",
          "gender": "female",
          "id": 3,
          "movie_id": 2,
          "name": "Sarah Chase"
        }
      ],
      "id": 2,
      "release_date": "Fri, 11 Mar 1977 00:00:00 GMT",
      "title": "Harold and Maude"
    },
    {
      "actors": [
        {
          "age": "43",
          "gender": "male",
          "id": 1,
          "movie_id": 3,
          "name": "Ray Charles"
        }
      ],
      "id": 3,
      "release_date": "Sat, 15 Jun 2013 00:00:00 GMT",
      "title": "Time Bandits"
    }
  ],
  "success": true
}
```



#### GET /movies/<int:id>

This endpoint should be accessable by all parties
and return a specified movie in json form.

```json
{
  "movies": [
    {
      "actors": [
        {
          "age": "23",
          "gender": "male",
          "id": 2,
          "movie_id": 1,
          "name": "Gus Demeter"
        }
      ],
      "id": 1,
      "release_date": "Tue, 06 Dec 1983 00:00:00 GMT",
      "title": "Jaws"
    },
  ],
  "success": true
}
```

#### POST /actors

This endpoint should be accessable by Casting Directors 
and Executive Producers only and return a list of actors including the newly added actor in json form.

```json
{
  "actors": [
    {
      "age": "43",
      "gender": "male",
      "id": 1,
      "movie_id": 3,
      "name": "Ray Charles"
    },
    {
      "age": "23",
      "gender": "male",
      "id": 2,
      "movie_id": 1,
      "name": "Gus Demeter"
    },
    {
      "age": "31",
      "gender": "female",
      "id": 3,
      "movie_id": 2,
      "name": "Sarah Chase"
    },
    {
      "age": "77",
      "gender": "female",
      "id": 4,
      "movie_id": 4,
      "name": "Susan Saranwrap"
    }
  ],
  "success": true
}
```

#### POST /movies

This endpoint should be accessable by Executive Producers only and return a list of movies including the newly added movie in json form.

```json
{
  "movies": [
    {
      "actors": [
        {
          "age": "23",
          "gender": "male",
          "id": 2,
          "movie_id": 1,
          "name": "Gus Demeter"
        }
      ],
      "id": 1,
      "release_date": "Tue, 06 Dec 1983 00:00:00 GMT",
      "title": "Jaws"
    },
    {
      "actors": [
        {
          "age": "31",
          "gender": "female",
          "id": 3,
          "movie_id": 2,
          "name": "Sarah Chase"
        }
      ],
      "id": 2,
      "release_date": "Fri, 11 Mar 1977 00:00:00 GMT",
      "title": "Harold and Maude"
    },
    {
      "actors": [
        {
          "age": "43",
          "gender": "male",
          "id": 1,
          "movie_id": 3,
          "name": "Ray Charles"
        }
      ],
      "id": 3,
      "release_date": "Sat, 15 Jun 2013 00:00:00 GMT",
      "title": "Time Bandits"
    },
    {
      "actors": [
        {
          "age": "77",
          "gender": "female",
          "id": 4,
          "movie_id": 4,
          "name": "Susan Saranwrap"
        }
      ],
      "id": 4,
      "release_date": "Mon, 01 Jan 2023 00:00:00 GMT",
      "title": "Clockwork Tangerine"
    }
  ],
  "success": true
}
```

#### PATCH /actors/<int:id>

This endpoint should be accessable by Casting Directors 
and Executive Producers only and should return a patched actor's information in json form


```json
{
  "actors": [
    {
      "age": "44",
      "gender": "male",
      "id": 1,
      "movie_id": 3,
      "name": "Ray Charles"
    }
  ],
  "success": true
}
```  

#### PATCH /movies/<int:id>

This endpoint should be accessable by Casting Directors 
and Executive Producers only and should return a patched movie's information in json form

```json
{
  "movies": [
    {
      "actors": [
        {
          "age": "23",
          "gender": "male",
          "id": 2,
          "movie_id": 1,
          "name": "Gus Demeter"
        },
        {
          "age": "10",
          "gender": "male",
          "id": 5,
          "movie_id": 1,
          "name": "Timmy O'Neil"
        }
      ],
      "id": 1,
      "release_date": "Tue, 06 Dec 1983 00:00:00 GMT",
      "title": "Jaws"
    },
  ],
  "success": true
}
```

#### DELETE /actors/<int:id>

This endpoint should be accessable by Casting Directors 
and Executive Producers only and should return information in json form

```json
{
    "deleted": 1,
    "success": true
}
```

#### DELETE /movies/<int:id>

This endpoint should be accessable by Executive Producers only and should return information in json form

```json
{
    "deleted": 1,
    "success": true
}
```

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
    "error": 401,
    "message": "Unauthorized",
    "success": false
}

```
The API will return four error types when requests fail:
- 401: Unauthorized
- 404: Resource Not Found
- 422: Unprocessable 
- 500: Internal Server Error