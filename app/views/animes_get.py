from flask import Blueprint

bp_hello = Blueprint('animes', __name__, url_prefix='/api')

# Em vez de @app, utilizamos a instancia de blueprint criada, bp_hello
@bp_hello.route('/animes', methods=['GET'])
def get_view():
    return {'data': 'hello'}