from flask import Blueprint, jsonify
from app.models.movies_models import Movies
import psycopg2

bp_movies = Blueprint('deleteMovie', __name__, url_prefix='/api')

@bp_movies.route('/movies/<int:movie_id>', methods=['DELETE'])
def filter(movie_id):
    try:
      processed_data = Movies.delete(movie_id)
      if processed_data == None:
        return {'error': 'Not found'}, 404
      return jsonify({"data": processed_data}), 200
    except (psycopg2.OperationalError, TypeError):
      return {'error': 'Not found'}, 404
 