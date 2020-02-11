import base64

from flask import Blueprint, render_template, jsonify, request, redirect, url_for, current_app
from werkzeug.utils import secure_filename

from database import mongo

mod = Blueprint("student", __name__)

def get_class_grade(student, class_name):
    """Return student's grade for class_name"""
    grade = student['classes'].get(class_name).get('grade')
    return (class_name, grade)


def get_class_subject(class_name):
    """Return the subject that class_name belongs to"""
    selected_class = mongo.db.classes.find_one({'name': class_name})
    return selected_class['subject']


def get_subjects_classes(student, subject="all"):
    """Return a dict of subjects and their classes for given student

    Keyword arguements:
    student -- The student you want subject and class information of
    subject -- Specific classes from a single subject. Default is all.
    """
    subjects_classes = {}
    for class_name in student['classes'].keys():
        selected_subject = get_class_subject(class_name)
        if subject == "all" or subject == selected_subject:
            if selected_subject not in subjects_classes:
                subjects_classes[selected_subject] = []
            subjects_classes[selected_subject].append(class_name)

    return subjects_classes


def get_average_grade(grades):
    """Return an average for a list of numbers"""
    return sum(grades)/len(grades)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.',1)[1].lower() in \
            current_app.config['ALLOWED_EXTENSIONS']

@mod.route('/')
def student_index():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    return render_template('student/index.html', student=student)


@mod.route('/update_profile', methods=['POST'])
def update_profile():
    student = mongo.db.users.find_one({'forename': 'Chris'})

    if student['profile_about'] != request.form.get('profile_about'):
        mongo.db.users.update_one({'forename': 'Chris'}, {'$set': {
            'profile_about': request.form.get('profile_about')}})

    new_image = request.files.get("profile_image")
    if new_image and allowed_file(new_image.filename):
        encoded_img = base64.b64encode(new_image.read()).decode()
        filetype = new_image.filename.rsplit('.',1)[1].lower() 
        img_data = f'data:image/{filetype};base64,{encoded_img}'
        mongo.db.users.update_one({'forename':'Chris'}, {'$set':{
            'profile_image': img_data
        }})
    return redirect(url_for('student.student_index'))


@mod.route('/classes')
def student_classes():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    menu_items = get_subjects_classes(student)
    return render_template('student/classes.html',
                           student=student,
                           menu_items=menu_items)


@mod.route('/_load_class_content')
def load_class_content():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    class_name = request.args.get('selected_class', "", type=str)
    selected_class = student['classes'].get(class_name.strip())
    return jsonify(class_name=class_name.strip(),
                   grade=selected_class.get('grade'),
                   day=selected_class.get('day'),
                   start_time=selected_class.get('start_time'),
                   finish_time=selected_class.get('finish_time'),
                   attendance=selected_class.get('attendance'))


@mod.route('/_load_subject_content')
def load_subject_content():
    student = mongo.db.users.find_one({'forename': 'Chris'})
    subject = request.args.get('subject', "", type=str).strip()
    student_classes = get_subjects_classes(student, subject)
    grades = [get_class_grade(student, current_class)
              for current_class in student_classes.get(subject)]
    average_grade = get_average_grade(grades)
    return jsonify(grades=grades, average_grade=average_grade)
