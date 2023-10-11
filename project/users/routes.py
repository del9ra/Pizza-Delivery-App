from flask import Blueprint, render_template, request, flash, redirect, url_for
from project import db
from project.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from helpers import apology

users = Blueprint('users', __name__)


@users.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return apology("must provide both username and password", 403)
        # filter all the users that have email
        user = User.query.filter_by(username=username).first()    # if we have unique result email, get first
        if user:
            # user.password from db, password is from the form
            if check_password_hash(user.hash, password):
                flash("You are logged in!", category='success')
                # remember: you don't need to log in everytime you go to the website, it remembers you
                login_user(user, remember=True)
                return redirect(url_for('main.index'))
            else:
                flash("The password you entered is incorrect. Please try again.", category='error')
        else:
            flash("This username does not exist.", category='error')
    return render_template("login.html", user=current_user)


@users.route("/logout")
@login_required     # it makes sure that we can't log out if the user is not logged in
def logout():
    logout_user()
    # redirect to the login page
    return redirect(url_for('users.login'))


@users.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        if not username or not password:
            return apology("must provide both username and password", 403)
        elif not confirmation:
            return apology("must enter password again", 403)
        user = User.query.filter_by(username=username).first()  # if we have unique result username, get first
        if user:    # check if it exists
            flash("Username already exists", category='error')
        elif password != confirmation:
            flash("Passwords don't match", category='error')
        else:
            # add user to the database. the user is defined in models.py
            new_user = User(username=username, hash=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # logged in after user creates account
            login_user(new_user, remember=True)
            flash("Welcome! Account created!", category="success")
            # redirect to the homepage. views is the name of file, home - of funct
            return redirect(url_for('main.index'))
    return render_template("signup.html", user=current_user)