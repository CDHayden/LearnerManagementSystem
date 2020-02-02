from flask import Blueprint, render_template, jsonify, request

from database import mongo

mod = Blueprint("student", __name__)


def get_class_subject(class_name):
    """Return the subject that class_name belongs to"""
    selected_class = mongo.db.classes.find_one({'name': class_name})
    return selected_class['subject']


def get_subjects_classes(student):
    """Return a dict of subjects and their classes for given student

    Keyword arguements:
    student -- The student you want subject and class information of
    """
    subjects_classes = {}
    for current_class in student['classes']:
        subject = get_class_subject(current_class['name'])
        if subject not in subjects_classes:
            subjects_classes[subject] = []
        subjects_classes[subject].append(current_class['name'])
    return subjects_classes


@mod.route('/')
def student_index():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    return render_template('student/index.html', student=student)


@mod.route('/classes')
def student_classes():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    menu_items = get_subjects_classes(student)
    return render_template('student/classes.html',
                           student=student,
                           menu_items=menu_items)


@mod.route('/_load_class_content')
def load_class_content():
    selected_class = request.args.get('selected_class', "", type=str)
    return jsonify(result=selected_class + " worked")