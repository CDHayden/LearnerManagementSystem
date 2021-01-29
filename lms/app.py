import os

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

import database
from .views.home import mod as home
from .views.student import mod as student
from .views.staff import mod as staff

def create_app(db_uri=None):
    #Load environment variables
    load_dotenv()

    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY")

    if not db_uri:
        app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
    else:
        app.config['MONGO_URI'] = db_uri 

    app.config['ALLOWED_EXTENSIONS'] = os.environ.get("ALLOWED_EXTENSIONS")
    database.mongo.init_app(app)

    app.register_blueprint(home)
    app.register_blueprint(student, url_prefix="/student")
    app.register_blueprint(staff, url_prefix="/staff")

    return app

