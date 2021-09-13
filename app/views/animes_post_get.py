import flask
import psycopg2
from flask import Blueprint, request, jsonify
from app.services.animes_services import Animes

bp_animes = Blueprint('animes', __name__, url_prefix='/api')

@bp_animes.route('/animes', methods=['POST', 'GET'])
def get_create():
  if flask.request.method == 'POST':
    try:
      data = request.json
      processed_data = Animes.post_anime(**data)
      if 'available_keys' in processed_data.keys():
        return processed_data, 422
      return jsonify(processed_data)
    except  psycopg2.errors.UniqueViolation:
       return jsonify({'error': 'anime already exists'}), 422
  else:
    try:
      processed_data = Animes.get_all_animes()
      return jsonify({"data": processed_data})
    except psycopg2.OperationalError: 
      return jsonify({"data": []}), 200

