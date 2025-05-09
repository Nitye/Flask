from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
      if check_password_hash(user.password, password):
        flash('Loggged in successfully.', category='success')
        login_user(user, remember=True)
        return redirect(f'/{user.first_name}/home')
      else:
        flash('Password doesn\'t match.', category='error')
    else:
      flash('Email isn\'t registered.', category='error')
  return render_template('login.html', user = None)

@auth.route('/logout')
@login_required
def logout():
  logout_user()
  return redirect(url_for('views.site_home'))

@auth.route('/sign-up', methods= ['GET','POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    name = request.form.get('name')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    user = User.query.filter_by(email=email).first()
    user2 = User.query.filter_by(first_name = name).first()
    if user:
      flash('Email already registered.', category='error')
    elif user2:
      flash('Name already taken.', category='error')
    elif len(email) <= 4:
      flash('Email must be greater than 4 characters.', category='error')
    elif len(name) <= 4:
      flash('Name must be greater than 4 characters.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    else:
      new_user = User(email=email, first_name = name, password = generate_password_hash(password1, method='sha256'))
      db.session.add(new_user)
      db.session.commit()
      flash('Account created and Logged in.', category='success')
      login_user(new_user, remember=True)
      return redirect(f'/{name}/home')
  return render_template('sign-up.html', user = None)