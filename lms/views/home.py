from flask import (Blueprint, render_template, request, redirect,
flash, session, url_for)
from bson.objectid import ObjectId

import database
from ..controllers.home_controller import log_user_in 

mod = Blueprint('home',__name__)

@mod.route('/')
def index():
    if session.get('user'):
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
            return redirect(url_for('student.student_index')) 
        
    flash("Login failed.")
    return redirect(url_for('home.index'))

@mod.route('/signout')
def signout():
    if session.get('user'):
        session.pop('user')

    return redirect(url_for('home.index'))

@mod.app_errorhandler(Exception)
def error_handler(e):
    return render_template('home/error.html')
