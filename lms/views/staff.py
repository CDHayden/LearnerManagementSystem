from flask import Blueprint, render_template

from database import mongo

mod = Blueprint("staff", __name__)

@mod.route('/')
def staff_index():
    return render_template('staff/index.html',
                            user = mongo.db.users.find_one())