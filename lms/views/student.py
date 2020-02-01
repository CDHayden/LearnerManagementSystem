from flask import Blueprint, render_template

from database import mongo

mod = Blueprint("student", __name__)

@mod.route('/')
def student_index():
    return render_template('student/index.html', student = mongo.db.users.find_one({'forename':'Chris'}))

@mod.route('/classes')
def student_classes():
    return render_template('student/classes.html', student = mongo.db.users.find_one({'forename':'Chris'}))