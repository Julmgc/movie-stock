import psycopg2
from flask import Blueprint, request
from app.services.animes_services import Animes

bp_animes = Blueprint('patchAnimes', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
  try:
    data = request.json
    processed_data = Animes.update_anime(anime_id, **data)
    return processed_data
  except psycopg2.DatabaseError:
     return {'error': 'Not found'}, 404





