import psycopg2
from flask import Blueprint, request
from app.models.movies_models import Movies

bp_movies = Blueprint('patchMovies', __name__, url_prefix='/api')

@bp_movies.route('/movies/<int:movie_id>', methods=['PATCH'])
def update(movie_id: int):
    try:
        data = request.json
        processed_data = Movies.update_movie(movie_id, **data)
        return processed_data
    except psycopg2.DatabaseError:
        return {'error': 'Not found'}, 404





