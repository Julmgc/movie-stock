from flask import Blueprint
import psycopg2
from app.models.movies_models import Movies

bp_movies = Blueprint('getById', __name__, url_prefix='/api')

@bp_movies.route('/movies/<int:movie_id>', methods=['GET'])
def filter(movie_id):
    try:
        processed_data = Movies.get_specific_movie(movie_id)
        if processed_data == None:
            return {'error': 'Not found'}, 404
        return {'data': [processed_data]}, 200
    except (psycopg2.OperationalError, TypeError):
        return {'error': 'Not found'}, 404

  
 