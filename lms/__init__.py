import os

from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv

from database import mongo
from .views.home import mod as home
from .views.student import mod as student
from .views.admin import mod as admin
from .views.staff import mod as staff

#Load environment variables
load_dotenv()

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")
app.config['MONGO_URI'] = os.environ.get("MONGO_URI")
app.config['ALLOWED_EXTENSIONS'] = os.environ.get("ALLOWED_EXTENSIONS")
mongo.init_app(app)

app.register_blueprint(home)
app.register_blueprint(student, url_prefix="/student")
app.register_blueprint(admin, url_prefix="/admin")
app.register_blueprint(staff, url_prefix="/staff")
