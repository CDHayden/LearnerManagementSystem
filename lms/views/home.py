from flask import (Blueprint, render_template, request, redirect,
flash, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash

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

# @mod.app_errorhandler(Exception)
# def error_handler(e):
    # return render_template('home/error.html')


@mod.route('/profile/<username>')
def public_profile(username):
    found_user = get_user_from_username(username) 
    if found_user:
        user = get_returnable_user(found_user)
    return render_template('home/profile.html', profile = user)

@mod.route('/populate_db')
def populate_db():
    database.mongo.db.users.insert_many([
            {
            '_id':ObjectId(),
            'username':'student1',
            'password':generate_password_hash('test'),
            'is_teacher':False,
            'forename':'chris',
            'surname':'hayden',
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[{'subject':'spanish','course':'speaking','grade':30}]
            }, 
            {
            '_id':ObjectId(),
            'username':'student2',
            'password':generate_password_hash('test'),
            'is_teacher':False,
            'forename':'bob',
            'surname':'loblaw',
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[{'subject':'spanish','course':'listening','grade':20},{'subject':'spanish','course':'speaking','grade':30}]
            },
            {
            '_id':ObjectId(),
            'username':'student3',
            'password':generate_password_hash('test'),
            'is_teacher':False,
            'forename':'miriam',
            'surname':'vilar',
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[{'subject':'english','course':'speaking','grade':100},{'subject':'german','course':'writing','grade':20}]
            },
            {
            '_id':ObjectId(),
            'username':'teacher1',
            'password':generate_password_hash('test'),
            'is_teacher':True,
            'forename':'Juan',
            'surname':'Carlos',
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[{'subject':'spanish','course':'speaking','grade':0},{'subject':'spanish','course':'listening','grade':0}]
            },
            {
            '_id':ObjectId(),
            'username':'teacher1',
            'password':generate_password_hash('test'),
            'is_teacher':True,
            'forename':'Saul',
            'surname':'Goodman',
            'profile_about': 'I need to update my profile',
            'profile_image': 'none',
            'subjects':[{'subject':'english','course':'speaking','grade':0},{'subject':'german','course':'writing','grade':0}]
            }]
            )
    return "Done"
