#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import sys
import dateutil.parser
import babel
from flask import (
    Flask, 
    render_template, 
    request, 
    Response, 
    flash, 
    redirect, 
    url_for
)
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
# Models can be viewed in models.py
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
  venue = Venue.query.get_or_404(venue_id)
  show = Show.query.join(Venue, Venue.id==Show.venue_id)
          
  past_shows = []
  upcoming_shows = []

  for show in venue.shows:
      data_show = {
        "artist_id": show.artist_id,
        "artist_name": Artist.query.get(show.artist_id).name,
        "artist_image_link": Artist.query.get(show.artist_id).image_link,
        "start_time":show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
      if show.start_time < datetime.now():
          past_shows.append(data_show)
      else:
          upcoming_shows.append(data_show)
  data= vars(venue)
    
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)
  
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(request.form)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form, meta={'csrf': False})
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # TODO: Done

  # on successful db insert, flash success
  # flash('Venue ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  if form.validate():
      try:
        venue = Venue(
           name=form.name.data,
           city=form.city.data,
           state=form.state.data,
           address=form.address.data,
           phone=form.phone.data,
           genres=form.genres.data,
           image_link=form.image_link.data,
           facebook_link=form.facebook_link.data,
           website_link=form.website_link.data,
           seeking_talent=form.seeking_talent.data,
           seeking_description=form.seeking_description.data
        )
        db.session.add(venue)
        db.session.commit()
      except ValueError as e:
        print(e)
        db.session.rollback()
      finally:
        db.session.close()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return render_template('pages/home.html')
  else:
      message = []
      for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
      flash('Please fix the following errors: ' + ', '.join(message))
      form = VenueForm()
      return render_template('forms/new_venue.html', form=form)


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

  artist = Artist.query.get_or_404(artist_id)
  show = Show.query.join(Artist, Artist.id==Show.artist_id)
  
  past_shows = []
  upcoming_shows = []

  for show in artist.shows:
      data_show={
        "venue_id": show.venue_id,
        "venue_name": Venue.query.get(show.venue_id).name,
        "venue_image_link": Venue.query.get(show.venue_id).image_link,
        "start_time": show.start_time.strftime("%m/%d/%Y, %H:%M")
        }
      if show.start_time < datetime.now():
          past_shows.append(data_show)
      else:
          upcoming_shows.append(data_show)
  data = vars(artist)
  
  data['past_shows'] = past_shows
  data['upcoming_shows'] = upcoming_shows
  data['past_shows_count'] = len(past_shows)
  data['upcoming_shows_count'] = len(upcoming_shows)

  return render_template('pages/show_artist.html', artist=data)
#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  
  artist = Artist.query.get(artist_id)
  form = ArtistForm(request.form)

  form.name.process_data(artist.name)
  form.city.process_data(artist.city)
  form.state.process_data(artist.state)
  form.phone.process_data(artist.phone)
  form.genres.process_data(artist.genres)
  form.facebook_link.process_data(artist.facebook_link)
  form.image_link.process_data(artist.image_link)
  form.website_link.process_data(artist.website_link)
  form.seeking_venue.process_data(artist.seeking_venue)
  form.seeking_description.process_data(artist.seeking_description)


  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes

  # TODO: Done

  artist = Artist.query.filter_by(id=artist_id).first_or_404()
  form = ArtistForm(request.form, meta={"csrf": False})
  
  try:
      artist = Artist.query.get(artist_id)

      artist.name = form.name.data
      artist.city = form.city.data
      artist.state = form.state.data
      artist.phone = form.phone.data
      artist.genres = request.form.getlist('genres')
      artist.facebook_link = form.facebook_link.data
      artist.image_link = form.image_link.data
      artist.website = form.website_link.data
      artist.seeking_venue = form.seeking_venue.data
      artist.seeking_description = form.seeking_description.data

      db.session.add(artist)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):

  venue = Venue.query.get(venue_id)
  form = VenueForm(request.form)

  form.name.process_data(venue.name)
  form.city.process_data(venue.city)
  form.state.process_data(venue.state)
  form.address.process_data(venue.address)
  form.phone.process_data(venue.phone)
  form.genres.process_data(venue.genres)
  form.facebook_link.process_data(venue.facebook_link)
  form.image_link.process_data(venue.image_link)
  form.website_link.process_data(venue.website_link)
  form.seeking_talent.process_data(venue.seeking_talent)
  form.seeking_description.process_data(venue.seeking_description)

  # TODO: populate form with values from venue with ID <venue_id>
  # TODO: Done

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):

  venue = Venue.query.filter_by(id=venue_id).first_or_404()
  form = VenueForm(request.form, meta={"csrf": False})
  
  try:
      venue = Venue.query.get(venue_id)

      venue.name = form.name.data
      venue.city = form.city.data
      venue.state = form.state.data
      venue.address = form.address.data
      venue.phone = form.phone.data
      venue.genres = request.form.getlist('genres')
      venue.facebook_link = form.facebook_link.data
      venue.image_link = form.image_link.data
      venue.website_link = form.website_link.data
      venue.seeking_talent = form.seeking_talent.data
      venue.seeking_description = form.seeking_description.data

      db.session.add(venue)
      db.session.commit()
  except:
      db.session.rollback()
  finally:
      db.session.close()

  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # TODO: Done
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(request.form)
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
  form = ArtistForm(request.form, meta={'csrf': False})
  
  if form.validate():
    try:
      artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        genres=form.genres.data,
        image_link=form.image_link.data,
        facebook_link=form.facebook_link.data,
        website_link=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_description=form.seeking_description.data 
      )
      db.session.add(artist) 
      db.session.commit()
    except ValueError as e:
      print(e)
      db.session.rollback()
    finally:
      db.session.close()
      flash('Artist ' + request.form['name'] + ' was successfully listed.')
      return render_template('pages/home.html')
  else:
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


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
  form = ShowForm(request.form)
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

  form = ShowForm(request.form, meta={'csrf': False})

  if form.validate():

    try:
        show = Show(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
        )
        db.session.add(show)
        db.session.commit()
    except ValueError as e:
        print(e)
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        flash("Show was successfully listed!")
        return render_template('pages/home.html')
  else:
    message = []
    for field, errors in form.errors.items():
        for error in errors:
            message.append(f"{field}: {error}")
    flash('Please fix the following errors: ' + ', '.join(message))
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)

    

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