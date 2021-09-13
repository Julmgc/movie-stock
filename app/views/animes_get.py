from flask import Blueprint

bp_hello = Blueprint('animes', __name__, url_prefix='/api')

@bp_hello.route('/animes', methods=['GET'])
def get_view():
    return {'data': 'hello'}