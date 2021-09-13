from flask import Flask

def init_app(app: Flask):
  from app.views.animes_post_get import bp_animes
  app.register_blueprint(bp_animes)

  from app.views.animes_id_get import bp_animes
  app.register_blueprint(bp_animes)

  from app.views.animes_id_delete import bp_animes
  app.register_blueprint(bp_animes)

  from app.views.animes_id_patch import bp_animes
  app.register_blueprint(bp_animes)
  
