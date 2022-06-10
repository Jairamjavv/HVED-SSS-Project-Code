from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
# used to maintain the sessions
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # query the db and return first result
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in!!!', category = 'success')
                # keeps the user in session memory until server restart or manual logout
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect Password', category = 'warning')
        else:
            flash('No User exists', category = 'warning')
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required # makes sure that the user is logged in and cannot be seen when no one is logged in
def logout():
    # logs out the current user and clears the login session for the current user
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password = request.form.get('password')
        checkPassword = request.form.get('checkPassword')
        
        user = User.query.filter_by(email=email).first()
        
        if user:
            flash('Email already exists. Please Login.', category='warning')
        if len(email) < 4:
            flash('Email should be greater than 4 characters',category='warning')
        elif len(firstName) < 2:
            flash('Name should be greater than 2 characters',category='warning')
        elif password != checkPassword:
            flash('Password is not matching. Check your password',category='warning')
        elif len(password) < 7:
            flash('Password length should be greater than 7 characters',category='warning')
        else:
            new_user = User(email=email, first_name=firstName, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()     
            login_user(new_user, remember=True)       
            flash('Yay! you are logged in.',category='success')
            return redirect(url_for('views.home'))
    return render_template("register.html", user=current_user)