import flask
from flask import Blueprint
import psycopg2
from app.services.animes_services import Animes

bp_animes = Blueprint('getById', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['GET'])
def filter(anime_id):
    try:
      processed_data = Animes.get_specific_anime(anime_id)
      if processed_data == None:
        return {'error': 'Not found'}, 404
      return {'data': [processed_data]}, 200
    except (psycopg2.OperationalError, TypeError):
      return {'error': 'Not found'}, 404

  
 