from flask import Blueprint
from app.services.animes_services import Animes
import psycopg2

bp_animes = Blueprint('deleteanime', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def filter(anime_id):
    try:
      processed_data = Animes.delete(anime_id)
      if processed_data == None:
        return {'error': 'Not found'}, 404
      return '', 204
    except (psycopg2.OperationalError, TypeError):
      return {'error': 'Not found'}, 404
 