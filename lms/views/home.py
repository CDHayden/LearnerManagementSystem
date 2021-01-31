from flask import (Blueprint, render_template, request, redirect,
flash, session, url_for)
from bson.objectid import ObjectId

import database
from ..controllers.home_controller import ( log_user_in, 
get_user_from_username,get_user_from_id, get_returnable_user )

mod = Blueprint('home',__name__)

@mod.route('/')
def index():
    user = session.get('user')
    if user:
        if get_user_from_id(user)['is_teacher']:
            return redirect(url_for('staff.staff_index'))
        else:
            return redirect(url_for('student.student_index'))

    return render_template('home/index.html')

@mod.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username and password:
        user = log_user_in(username, password)
        if user:
            session['user'] = user['id']
            if user['is_teacher']:
                return redirect(url_for('staff.staff_index')) 
            else:
                return redirect(url_for('student.student_index')) 
        
    flash("Login failed","alert-danger")
    return redirect(url_for('home.index'))

@mod.route('/signout')
def signout():
    if session.get('user'):
        session.pop('user')

    return redirect(url_for('home.index'))

@mod.app_errorhandler(Exception)
def error_handler(e):
    return render_template('home/error.html')


@mod.route('/profile/<username>')
def public_profile(username):
    found_user = get_user_from_username(username) 
    if found_user:
        user = get_returnable_user(found_user)
    return render_template('home/profile.html', profile = user)
