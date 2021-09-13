import flask
from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.route('/animes', methods=['POST', 'GET'])
def get_create():
  if flask.request.method == 'POST':
    try:
      data = request.json
      processed_data = Animes.post_anime(**data)
      return jsonify(processed_data)
    except Exception as e:
      return str(e)
  else:
    try:
      processed_data = Animes.get_all_animes()
      return jsonify(processed_data)
    except:
      return {[]}, 200

