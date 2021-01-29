from flask import Blueprint, render_template, session

import database
from ..controllers.user_controller import get_user_by_id
mod = Blueprint("staff", __name__)

@mod.route('/')
def staff_index():
    staff = get_user_by_id(session['user'])
    return render_template('staff/index.html', user = staff)

@mod.route('/my_classes')
def staff_classes():
    return "Classes"

@mod.route('/manage_students')
def manage_students():
    return "students"
