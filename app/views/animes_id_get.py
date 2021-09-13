import flask
from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('getbyid', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['GET'])
def filter(anime_id):
    try:
      processed_data = Animes.get_specific_anime(anime_id)
      return processed_data
    except Exception as e:
      return str(e)
 