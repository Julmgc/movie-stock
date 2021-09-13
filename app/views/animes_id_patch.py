import flask
from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('patchAnimes', __name__, url_prefix='/api')

@bp_animes.route('/animes/<int:anime_id>', methods=['PATCH'])
def update(anime_id: int):
  try:
    data = request.json
    processed_data = Animes.update_anime(anime_id, **data)
    return processed_data
  except Exception as e:
    return str(e), 404
      # se a table estiver vazia return an empy dicty with a list inside, 200
    # otherwise return the dict list, 200




