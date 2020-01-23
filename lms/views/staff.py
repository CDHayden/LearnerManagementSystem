from flask import Blueprint, render_template

mod = Blueprint("staff", __name__)

@mod.route('/')
def staff_index():
    return render_template('staff/index.html')