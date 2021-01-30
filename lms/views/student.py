from sys import stderr
from flask import ( Blueprint, render_template, jsonify, request,  
    redirect, url_for, flash, session)

from database import mongo
from ..controllers.user_controller import (get_user_by_name,
       update_user_profile, get_user_by_id, generate_menu_items) 

mod = Blueprint("student", __name__)


@mod.route('/')
def student_index():
    student = get_user_by_id(session['user'])
    return render_template('student/index.html',student=student)


@mod.route('/update_profile', methods=['POST'])
def update_profile():
    student = get_user_by_id(session['user'])
    data = {'profile_about':request.form.get('profile_about'),
            'profile_img': request.files.get('profile_image')}
    message = update_user_profile(student.id,data)
    flash(message[0],message[1])

    return redirect(url_for('student.student_index'))


@mod.route('/courses')
def student_courses():
    student = get_user_by_id(session['user'])
    menu_items = generate_menu_items(session['user'])
    return render_template('student/courses.html',
                           student=student,
                           menu_items=menu_items)


@mod.route('/_load_course_content', methods=['POST'])
def load_course_content():
    student = get_user_by_id(session['user'])
    subject = request.json['subject']
    course = request.json['course']
    content = student.subjects[subject][course];
    return content

@mod.route('/_load_subject_content', methods=['POST'])
def load_subject_content():
    student = get_user_by_id(session['user'])
    data = student.get_subject_content(request.json['subject'])
    return data
