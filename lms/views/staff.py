from flask import ( Blueprint, render_template, jsonify, request,  
    redirect, url_for, flash, session)

import database
from ..controllers.user_controller import (get_user_by_id,
update_user_profile, get_students_of_course, generate_menu_items, 
get_user_by_username, get_students_not_of_course)

mod = Blueprint("staff", __name__)

@mod.route('/')
def staff_index():
    staff = get_user_by_id(session['user'])
    return render_template('staff/index.html', user = staff)

@mod.route('/my_classes')
def staff_classes():
    staff = get_user_by_id(session['user'])
    return render_template('staff/staffclasses.html', user = staff, 
            menu_items = generate_menu_items(staff._id))

@mod.route('/manage_students')
def manage_students():
    students = get_students_of_course('spanish','speaking')
    return render_template('staff/managestudents.html', students = students)

@mod.route('/update_profile', methods=['POST'])
def update_staff_profile():
    staff = get_user_by_id(session['user'])
    data = {'profile_about':request.form.get('profile_about'),
            'profile_img': request.files.get('profile_image')}
    message = update_user_profile(staff.id,data)
    flash(message[0],message[1])

    return redirect(url_for('staff.staff_index'))

@mod.route('/_load_class',methods=['POST'])
def load_class():
    return jsonify( get_students_of_course(request.json['subject'],request.json['course']) )

@mod.route('/_edit_student',methods=['POST'])
def edit_student_in_class():
    username = request.form['username']
    grade = request.form['grade']
    subject = request.form['subject']
    course = request.form['course']

    if username and grade and subject and course:
        user = get_user_by_username(username)
        if user:
            user.add_course(subject,course,grade)
            flash(f'Updated {username}\'s grade to {grade}','alert-success')
            return redirect(url_for('staff.staff_classes'))

    flash(f'Could not update {username}\'s {grade}','alert-warning')
    return redirect(url_for('staff.staff_classes'))


@mod.route('/_delete_student', methods=['POST'])
def delete_student_in_class():
    username = request.form['username']
    subject = request.form['subject']
    course = request.form['course']
    if username and subject and course:
        user = get_user_by_username(username)
        if user:
            user.delete_course(subject,course)
            flash(f'{username} removed from {subject} - {course}','alert-success')
            return redirect(url_for('staff.staff_classes'))

    flash(f'Could not remove {username} from {subject} - {course}','alert-danger')
    return redirect(url_for('staff.staff_classes'))

@mod.route('_add_students', methods=['POST'])
def add_student_in_class():
    students = request.form.getlist('students')
    subject = request.form['subject']
    course = request.form['course']

    if students and subject and course:
        for student in students:
            get_user_by_username(student).add_course(subject,course)
        flash(f"Successfully added {students} to {subject}-{course}","alert-success")
        return redirect(url_for('staff.staff_classes'))

    flash(f"Could not add {students}","alert-danger")
    return redirect(url_for('staff.staff_classes'))

@mod.route('_get_students_not_in_course', methods=['POST'])
def get_students_not_in_course():
    subject = request.json['subject']
    course = request.json['course']
    students = get_students_not_of_course(subject,course)
    return jsonify(students)

@mod.route('_add_class',methods=['POST'])
def add_class():
    subject = request.form['subject']
    course = request.form['course']
    user = get_user_by_id(session['user'])
    user.add_course(subject,course)
    return redirect(url_for('staff.staff_classes'))

@mod.route('_delete_class',methods=['POST'])
def delete_class():
    subject = request.form['subject']
    course = request.form['course']

    #Remove the course from any students
    names = get_students_of_course(subject,course)
    for name in names:
        user = get_user_by_username(name['username'])
        user.delete_course(subject, course);

    user = get_user_by_id(session['user'])
    user.delete_course(subject,course)
    return redirect(url_for('staff.staff_classes'))
