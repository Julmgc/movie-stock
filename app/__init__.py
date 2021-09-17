from flask import Flask
from app import controllers

def create_app():
    app = Flask(__name__)
    controllers.init_app(app)

    return app