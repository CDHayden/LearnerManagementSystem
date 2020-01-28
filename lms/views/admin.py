from flask import Blueprint, render_template

from database import mongo

mod = Blueprint("admin", __name__)

@mod.route('/')
def admin_index():
    return render_template('admin/index.html', user = mongo.db.users.find_one())
