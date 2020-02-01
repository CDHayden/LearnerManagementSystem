from flask import Blueprint, render_template
from bson.objectid import ObjectId

from database import mongo

mod = Blueprint('home',__name__)

@mod.route('/')
def index():
    return render_template('home/index.html')

@mod.route('/profile/<user_id>')
def public_profile(user_id):
    found_user = mongo.db.users.find_one({'_id':ObjectId(user_id)})
    return render_template('home/profile.html', profile = found_user)