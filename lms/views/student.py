from flask import Blueprint, render_template

from database import mongo

mod = Blueprint("student", __name__)

@mod.route('/')
def student_index():
    return render_template('student/index.html', user = mongo.db.users.find_one())