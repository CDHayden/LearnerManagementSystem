import os

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

import database
from .views.home import mod as home
from .views.student import mod as student
from .views.admin import mod as admin
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
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(staff, url_prefix="/staff")

    return app

# if __name__ == "__main__":
    # host = os.environ.get("HOST","127.0.0.1")
    # port = os.environ.get("PORT","5050")

    # app.run(host, port)
