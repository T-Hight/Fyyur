#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime
from models import db, Artist, Venue, Show
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database
# TODO: Done

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  # TODO: Done

  locals=[]
  venues = Venue.query.all()
  places = Venue.query.distinct(Venue.city, Venue.state).all()

  for place in places:
    locals.append({
        'city': place.city,
        'state': place.state,
        'venues': [{
            'id': venue.id,
            'name': venue.name,
            'num_upcoming_shows': len([show for show in venue.shows if show.start_time > datetime.now()])
              } for venue in venues if
                  venue.city == place.city and venue.state == place.state]
    })
  
  return render_template('pages/venues.html', areas=locals)

@app.route('/venues/search', methods=['POST', 'GET'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # TODO: Done
  search_term = request.form.get('search_term', '')
  result = Venue.query.filter(Venue.name.ilike(f'%{search_term}%'))
  response = {
        "count": result.count(),
        "data": result
    }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # TODO: Done
    venue = Venue.query.get(venue_id)

    past_shows = db.session.query(Artist, Show).\
        join(Show).join(Venue).\
        filter (
            Show.venue_id == venue.id,
            Show.artist_id == Artist.id,
            Show.start_time < datetime.now()
        ).\
        all()

    upcoming_shows = db.session.query(Artist, Show).\
        join(Show).join(Venue).\
        filter(
            Show.venue_id == venue_id,
            Show.artist_id == Artist.id,
            Show.start_time > datetime.now()
        ).\
        all()

    venue = Venue.query.filter_by(id=venue_id).first_or_404()

    data = {
        'name': venue.name,
        'id': venue.id,
        #'genres': venue.genres,
        'address': venue.address,
        'city': venue.city,
        'state': venue.state,
        'phone': venue.phone,
        'website': venue.website_link,
        'facebook_link': venue.facebook_link,
        'seeking_talent': venue.seeking_talent,
        'image_link': venue.image_link,
        'past_shows': [{
            'artist_id': artist.id,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in past_shows],
        'upcoming_shows': [{
            'artist_id': artist.id,
            'artist_name': artist.name,
            'artist_image_link': artist.image_link,
            'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
        } for artist, show in upcoming_shows],
        'past_shows_count': len(past_shows),
        'upcoming_shows_count': len(upcoming_shows)
    }

    return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # TODO: Done

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  error = False

  try:
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
  except:
     error=True
  finally:
     if not error:
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
     else:
        flash('An error occurred. Venue ' + venue.name + ' could not be listed.')
        db.session.rollback()

  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  # TODO: Done
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  try:
     venue = Venue.query.filter_by(id=venue_id).first_or_404()
     db.session.delete(venue)
     db.session.commit()
     flash("The venue has been removed together with all of it's shows")
     return render_template('pages/home.html')
  except ValueError:
     flash('It was not possible to delete this venue.')
  return redirect(url_for('venues'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # TODO: Done
  data = Artist.query.all()
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  # TODO: Done

  search_term = request.form.get('search_term', '')
  result = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response={
    "count": result.count(),
    "data": result
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # TODO: Done

  artist = Artist.query.get(artist_id)

  past_shows = db.session.query(Venue, Show).\
      join(Show).join(Artist).\
      filter (
          Show.artist_id == artist.id,
          Show.venue_id == Venue.id,
          Show.start_time > datetime.now()
      ).\
      all()

  upcoming_shows = db.session.query(Venue, Show).\
      join(Show).join(Artist).\
      filter(
          Show.artist_id == artist.id,
          Show.venue_id == Venue.id,
          Show.start_time > datetime.now()
      ).\
      all()
  
  artist = Artist.query.filter_by(id=artist_id).first_or_404()

  data = {
      'id': artist.id,
      'name': artist.name,
      'genres': artist.genres,
      'city': artist.city,
      'state': artist.state,
      'phone': artist.phone,
      'website': artist.website_link,
      #'seeking_talent': artist.seeking_talent,
      'image_link': artist.image_link,
      'past_shows': [{
          'venue_id': venue.id,
          "venue_name": venue.name,
          "venue_image_link": venue.image_link,
          "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for venue, show in past_shows],
      'upcoming_shows': [{
          'venue_id': venue.id,
          'venue_name': venue.name,
          'venue_image_link': venue.image_link,
          'start_time': show.start_time.strftime("%m/%d/%Y, %H:%M")
      } for venue, show in upcoming_shows],
      'past_shows_count': len(past_shows),
      'upcoming_shows_count': len(upcoming_shows)
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  # artist= 
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # Not Done

  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  form = ArtistForm(request.form, meta={"csrf": False})
  if form.validate():
    try:
        artist.name = form.name.data,
        artist.city = form.city.data,
        artist.state = form.state.data,
        artist.phone = form.phone.data,
        artist.genres = form.genres.data,
        artist.facebook_link = form.facebook_link.data,
        artist.image_link = form.image_link.data,
        artist.website = form.website_link.data,
        artist.seeking_venue = form.seeking_venue.data,
        artist.seeking_description = form.seeking_description.data
        db.session.commit()
        flash('The Artist ' + request.form['name'] + ' has been successfully updated!')
    except ValueError as e:
          print(e)
          print(sys.exc_info())
          db.session.rollback()
          flash('Error! Artist could not be updated.')
    finally:
          db.session.close()
  else:
      message = []
      for field, errors in form.errors.items():
          message.append(form[field].label + ', '.join(errors))
          flash('Errors: ' + '|'.join(message))

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # on successful db insert, flash success
  # flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  # TODO: Done
  form = ArtistForm(request.form)
  error = False
  
  try:
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist) 
  except:
      error = True
  finally:
      if not error:
          db.session.commit()
          flash('Artist ' + request.form['name'] + ' was successfully listed.')
      else:
          flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
          db.session.rollback()
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  # TODO: Done

  data=[]
  shows = Show.query.order_by(Show.start_time.desc()).all()
  for show in shows:
     venue = Venue.query.filter_by(id=show.venue_id).first_or_404()
     artist = Artist.query.filter_by(id=show.artist_id).first_or_404()
     data.extend([{
        "venue_id": venue.id,
        "venue_name": venue.name,
        "artist_id": artist.id,
        "artist_name": artist.name,
        "artist_image_link": artist.image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
     }])
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # TODO: Done

  error = False
  form = request.form

  try:
      artist_id = form['artist_id']
      venue_id = form['venue_id']
      start_time = form['start_time']
      show = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      db.session.add(show)
  except ValueError as e:
      print(e)
      error = True
      print(sys.exc_info())
  finally:
      if not error:
          flash("Show was successfully listed!")
          db.session.commit()
      else:
          flash("An error occurred. Show could not be listed.")
          db.session.rollback()
          db.session.close()

  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
