from flask import Flask

def init_app(app: Flask):
  from app.controllers.movies_post_get import bp_movies
  app.register_blueprint(bp_movies)

  from app.controllers.movies_id_get import bp_movies
  app.register_blueprint(bp_movies)

  from app.controllers.movies_id_delete import bp_movies
  app.register_blueprint(bp_movies)

  from app.controllers.movies_id_patch import bp_movies
  app.register_blueprint(bp_movies)
  
