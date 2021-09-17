import flask
import psycopg2
from flask import Blueprint, request, jsonify
from app.models.movies_models import Movies

bp_movies = Blueprint('movies', __name__, url_prefix='/api')

@bp_movies.route('/movies', methods=['POST', 'GET'])
def get_create():
  if flask.request.method == 'POST':
    try:
      data = request.json
      processed_data = Movies.post_movie(**data)
      if 'available_keys' in processed_data.keys():
        return processed_data, 422
      return processed_data
    except  psycopg2.errors.UniqueViolation:
       return jsonify({'error': 'movie already exists'}), 422
    except IndexError:
      return jsonify({'error': 'Please send movie, seasons and released_date data'})
  else:
    try:
      processed_data = Movies.get_all_movies()
      return jsonify({"data": processed_data})
    except psycopg2.OperationalError: 
      return jsonify({"data": []}), 200

