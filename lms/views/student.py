from flask import Blueprint, render_template

mod = Blueprint("student", __name__)

@mod.route('/')
def student_index():
    return render_template('student/index.html')