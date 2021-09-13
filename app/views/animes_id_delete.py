import flask
from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('deleteanime', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['DELETE'])
def filter(anime_id):
    try:
      processed_data = Animes.delete(anime_id)
      if  not processed_data:
        return {}, 404
      return '', 204
    except Exception as e:
      return str(e)
 